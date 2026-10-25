import hmac
import json
import os
from urllib.parse import parse_qs

from google import genai
from google.genai import types
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from supabase import create_client

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

SYSTEM_INSTRUCTION = (
    "You are a backend RPG data referee. Do not write creative narratives. "
    "Determine the mechanical outcome and output hidden facts that their character "
    "can visibly discover. You must return a valid JSON object with the properties: "
    "success (boolean), supabasePayload (string), and visibleFactsForPlayer (string)."
)

mcp = FastMCP(
    "multi-player-mcp-engine",
    stateless_http=True,
    json_response=True,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=["multi-player-mcp-engine-sand.vercel.app", "localhost:*", "127.0.0.1:*"],
        allowed_origins=["https://multi-player-mcp-engine-sand.vercel.app", "https://claude.ai"],
    ),
)

@mcp.tool()
def submit_action(playerId: str, characterAction: str) -> str:
    """Submit your character action to the world game master."""
    global_state = supabase.table("game_state").select("*").execute().data
    rows = supabase.table("players").select("*").eq("id", playerId).limit(1).execute().data
    player = rows[0] if rows else None

    prompt = (
        f"Player ID: {playerId}\n"
        f"Character Action: {characterAction}\n"
        f"Character Sheet: {json.dumps(player)}\n"
        f"World State: {json.dumps(global_state)}\n"
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
        ),
    )
    data = json.loads(response.text or "{}")

    # Optional: apply data["supabasePayload"] to Supabase here

    return data.get("visibleFactsForPlayer") or "Action evaluated."


API_KEY = os.environ.get("MCP_API_KEY", "")

class ApiKeyMiddleware:
    """Reject every HTTP request that does not carry the shared API key.

    The key can be sent as `Authorization: Bearer <key>`, `x-api-key: <key>`
    or `?key=<key>` in the URL (custom connectors in Claude only let you set a URL).
    Fails closed: with no MCP_API_KEY configured, every request is rejected.
    Uses 403, not 401, so clients do not start an OAuth sign-in flow.
    """

    def __init__(self, app):
        self.app = app

    def _authorized(self, scope) -> bool:
        if not API_KEY:
            return False
        headers = {k.decode().lower(): v.decode() for k, v in scope.get("headers", [])}
        candidates = [headers.get("x-api-key", "")]
        auth = headers.get("authorization", "")
        if auth.lower().startswith("bearer "):
            candidates.append(auth[7:].strip())
        query = parse_qs(scope.get("query_string", b"").decode())
        candidates.extend(query.get("key", []))
        return any(hmac.compare_digest(c.encode(), API_KEY.encode()) for c in candidates if c)

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and not self._authorized(scope):
            body = b'{"error":"forbidden"}'
            await send({"type": "http.response.start", "status": 403,
                        "headers": [(b"content-type", b"application/json"),
                                    (b"content-length", str(len(body)).encode())]})
            await send({"type": "http.response.body", "body": body})
            return
        await self.app(scope, receive, send)  # lifespan events pass straight through


# ASGI app served by Vercel; the MCP endpoint is /mcp
app = ApiKeyMiddleware(mcp.streamable_http_app())
