"""Illustrations: generation (Cloudflare Workers AI, FLUX.2 klein), storage (Supabase Storage, private bucket) and short-lived links.
The image bytes live in the bucket. The database holds only a record (`gm_images`): the prompt, who may see it, its status and its path."""
import base64
import io
import json
import os
import urllib.error
import urllib.request
import uuid

from . import config


class ImageError(Exception):
    pass


def _multipart(fields, files):
    """A multipart/form-data body (FLUX.2 on Workers AI only accepts multipart, even for a prompt alone)."""
    boundary = "----gm" + uuid.uuid4().hex
    out = []
    for k, v in fields.items():
        out.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for k, (fname, data, ctype) in files.items():
        out.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"; filename="{fname}"\r\nContent-Type: {ctype}\r\n\r\n'.encode())
        out.append(data)
        out.append(b"\r\n")
    out.append(f"--{boundary}--\r\n".encode())
    return b"".join(out), f"multipart/form-data; boundary={boundary}"


def sniff(data):
    if data[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    return "image/jpeg"


def fit_square(data, size, quality=90):
    """Re-encodes an image as a JPEG of exactly size x size (references must be small, and the output sizes must be uniform)."""
    from PIL import Image
    im = Image.open(io.BytesIO(data)).convert("RGB")
    if im.size != (size, size):
        im = im.resize((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality)
    return buf.getvalue()


def fit_max(data, size, quality=82):
    """Reduces an image so its longest side is at most `size` (for pictures sent inline in a chat), as a JPEG."""
    from PIL import Image
    im = Image.open(io.BytesIO(data)).convert("RGB")
    if max(im.size) > size:
        r = size / max(im.size)
        im = im.resize((max(1, round(im.size[0] * r)), max(1, round(im.size[1] * r))), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality)
    return buf.getvalue()


def overlay_name(data, name, quality=90):
    """Writes the name on a band at the bottom of the picture. Done here because image models cannot spell reliably."""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.open(io.BytesIO(data)).convert("RGBA")
    w, h = im.size
    size = max(18, h // 16)
    font = ImageFont.load_default(size=size)
    draw = ImageDraw.Draw(im)
    text = name.strip()[:60]
    while size > 12 and draw.textlength(text, font=font) > w * 0.9:
        size -= 2
        font = ImageFont.load_default(size=size)
    band_h = int(size * 1.9)
    band = Image.new("RGBA", (w, band_h), (0, 0, 0, 150))
    im.alpha_composite(band, (0, h - band_h))
    draw = ImageDraw.Draw(im)
    tw = draw.textlength(text, font=font)
    draw.text(((w - tw) / 2, h - band_h + (band_h - size) / 2 - size * 0.1), text, font=font, fill=(245, 240, 225, 255))
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=quality)
    return buf.getvalue()


class CloudflareFlux:
    """FLUX.2 klein on Workers AI. POST /accounts/{id}/ai/run/{model}, multipart: prompt, width, height and up to four reference
    images named input_image_0..3 (each at most 512x512). The image comes back base64."""

    MAX_REFS = 4

    @staticmethod
    def configured():
        return bool(os.environ.get("CLOUDFLARE_ACCOUNT_ID") and os.environ.get("CLOUDFLARE_API_TOKEN"))

    def _call(self, prompt, width, height, refs, timeout):
        acct, token = os.environ["CLOUDFLARE_ACCOUNT_ID"], os.environ["CLOUDFLARE_API_TOKEN"]
        url = f"https://api.cloudflare.com/client/v4/accounts/{acct}/ai/run/{config.IMAGE_MODEL}"
        files = {f"input_image_{i}": (f"ref{i}.jpg", d, "image/jpeg") for i, d in enumerate(refs[:self.MAX_REFS])}
        body, ctype = _multipart({"prompt": prompt[:2048], "width": str(width), "height": str(height)}, files)
        req = urllib.request.Request(url, data=body, headers={"Authorization": f"Bearer {token}", "Content-Type": ctype})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            rtype = r.headers.get("Content-Type", "")
        if rtype.startswith("image/"):
            return raw
        data = json.loads(raw)
        res = data.get("result", data) if isinstance(data, dict) else {}
        b64 = res.get("image") if isinstance(res, dict) else None
        if not b64:
            raise ImageError("the image provider returned no image")
        return base64.b64decode(b64)

    def generate(self, prompt, width=None, height=None, refs=None, timeout=None):
        """Returns (jpeg bytes, "image/jpeg") at exactly width x height. `refs` are image bytes. If the provider rejects the
        references, one retry is made with smaller ones."""
        width = width or config.IMAGE_SIZE
        height = height or config.IMAGE_SIZE
        timeout = timeout or config.IMAGE_TIMEOUT_SECONDS
        refs = [fit_square(r, config.IMAGE_REF_SIZE) for r in (refs or [])]
        try:
            try:
                raw = self._call(prompt, width, height, refs, timeout)
            except urllib.error.HTTPError as e:
                if e.code not in (400, 422) or not refs:
                    raise
                raw = self._call(prompt, width, height, [fit_square(r, config.IMAGE_REF_SIZE - 64) for r in refs], timeout)
        except ImageError:
            raise
        except Exception as e:
            raise ImageError(f"image provider error ({type(e).__name__}{': ' + str(e.code) if hasattr(e, 'code') else ''})") from None
        im_w, im_h = _size(raw)
        if (im_w, im_h) != (width, height):
            from PIL import Image
            im = Image.open(io.BytesIO(raw)).convert("RGB").resize((width, height), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=90)
            raw = buf.getvalue()
        return raw, sniff(raw)


def _size(data):
    from PIL import Image
    return Image.open(io.BytesIO(data)).size


class SupabaseImageStorage:
    """A private bucket. The server uses the service role to write and to sign links. A link is the only way to see an image."""

    def __init__(self, client, bucket=None):
        self.sb = client
        self.bucket = bucket or config.IMAGE_BUCKET

    def put(self, path, data, content_type):
        self.sb.storage.from_(self.bucket).upload(path, data, {"content-type": content_type, "upsert": "true"})

    def get(self, path):
        return self.sb.storage.from_(self.bucket).download(path)

    def signed_url(self, path, ttl):
        r = self.sb.storage.from_(self.bucket).create_signed_url(path, ttl)
        u = r.get("signedURL") or r.get("signedUrl") or ""
        if u.startswith("/"):
            u = os.environ.get("SUPABASE_URL", "").rstrip("/") + "/storage/v1" + u
        return u

    def delete(self, path):
        self.sb.storage.from_(self.bucket).remove([path])


class MemoryImageStorage:
    def __init__(self):
        self.files = {}

    def put(self, path, data, content_type):
        self.files[path] = (data, content_type)

    def get(self, path):
        return self.files[path][0]

    def signed_url(self, path, ttl):
        return f"https://storage.example/sign/{path}?expires_in={ttl}"

    def delete(self, path):
        self.files.pop(path, None)


class ImageService:
    def __init__(self, provider, storage, usage):
        self.provider = provider
        self.storage = storage
        self.usage = usage

    @property
    def configured(self):
        return bool(self.provider and self.provider.configured())
