"""Illustrations: generation (Cloudflare Workers AI, Flux), storage (Supabase Storage, private bucket) and short-lived links.
The image bytes live in the bucket. The database holds only a record (`gm_images`): the prompt, who may see it, its status and its path."""
import base64
import json
import os
import urllib.request

from . import config


class ImageError(Exception):
    pass


class CloudflareFlux:
    """FLUX.1 schnell on Workers AI. POST /accounts/{id}/ai/run/{model} with {prompt, steps}; the image comes back base64 (JPEG)."""

    @staticmethod
    def configured():
        return bool(os.environ.get("CLOUDFLARE_ACCOUNT_ID") and os.environ.get("CLOUDFLARE_API_TOKEN"))

    def generate(self, prompt):
        acct, token = os.environ["CLOUDFLARE_ACCOUNT_ID"], os.environ["CLOUDFLARE_API_TOKEN"]
        url = f"https://api.cloudflare.com/client/v4/accounts/{acct}/ai/run/{config.IMAGE_MODEL}"
        body = json.dumps({"prompt": prompt[:2048], "steps": config.IMAGE_STEPS}).encode()
        req = urllib.request.Request(url, data=body, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=config.IMAGE_TIMEOUT_SECONDS) as r:
                data = json.loads(r.read())
        except Exception as e:
            raise ImageError(f"image provider error ({type(e).__name__})") from None
        res = data.get("result", data) if isinstance(data, dict) else {}
        b64 = res.get("image") if isinstance(res, dict) else None
        if not b64:
            raise ImageError("the image provider returned no image")
        return base64.b64decode(b64), "image/jpeg"


class SupabaseImageStorage:
    """A private bucket. The server uses the service role to write and to sign links. A link is the only way to see an image."""

    def __init__(self, client, bucket=None):
        self.sb = client
        self.bucket = bucket or config.IMAGE_BUCKET

    def put(self, path, data, content_type):
        self.sb.storage.from_(self.bucket).upload(path, data, {"content-type": content_type, "upsert": "true"})

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
