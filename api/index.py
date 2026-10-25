import json
import os

from google import genai
from google.genai import types
from mcp.server.fastmcp import FastMCP
from supabase import create_client

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

SYSTEM_INSTRUCTION = (
    "You are a backend RPG data referee. Do not write creative narratives. "
    "Determine the mechanical outcome and output hidden facts that their character "
    "can visibly discover. You must return a valid JSON object with the properties: "
    "success (boolean), supabasePayload (string), and visibleFactsForPlayer (string)."
)

mcp = FastMCP("multi-player-mcp-engine", stateless_http=True, json_response=True)


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


# ASGI app served by Vercel; the MCP endpoint is /mcp
app = mcp.streamable_http_app()
