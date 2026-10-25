# multi-player-mcp-engine

- Each player uses his own free Claude account with MCP connectors, and uses Claude desktop, claude web or claude android as front end.
- The game state is stored in supabase.
- The MCP servers are run in Vercel.
- The AI Master is Google AI Studio (model Gemini 2.5 Pro).

1. Claude -> Vercel (HTTP POST / SSE): Claude contacts Vercel via a standard HTTP POST request. Vercel leaves that request open and uses Server-Sent Events (SSE) to stream the text blocks. The payload wrapped inside this stream strictly follows the open-source MCP JSON-RPC 2.0 protocol standard.

2. Vercel -> Supabase (JSON): Vercel uses the official Supabase Node.js SDK, which communicates entirely via RESTful API calls. Data going to Supabase and rows returning from Supabase are structured as standard javascript/JSON objects.

3. Vercel -> AI Studio (JSON): Vercel uses Google's Gen AI SDK. The prompt text, system logic, and the critical structural instructions are bundled into a JSON payload sent over HTTPS to Google.

4. AI Studio -> Vercel (JSON): Instead of generating full storytelling paragraphs, Gemini 2.5 Pro outputs raw, perspective-bounded facts for that specific player.
	• Example Output: {"success": true, "hp_change": 0, "visible_event": "You successfully pickpocketed the silver key from the sleeping guard without waking him. The guard is still breathing heavily."}

5. Vercel -> Supabase (JSON): Vercel updates the database (e.g., adding the "Silver Key" to the player's inventory array).

6. Vercel -> Claude (JSON): Vercel packages Gemini's visible_event facts directly into the MCP JSON-RPC wrapper and streams it back over the open SSE connection.
	• Example Payload: {"content": [{"type": "text", "text": "METADATA RESULT: Success. Target: Sleeping Guard. Item obtained: Silver Key. Guard status: Unaware."}]}

7. Claude User Interface: The player's Claude instance reads that synthetic metadata block from the tool. Because Claude acts as an intelligent agent, it consumes that structured data as a "ground truth fact" and writes the cinematic narrative for the player:
	• Claude's Output: "Holding your breath, you slip your fingers into the guard's rusted chainmail pouch. Your knuckles brush against cold metal as you carefully slide out a heavy silver key. The guard snorts and rolls over, but his deep snores continue. You step back into the shadows, key in hand."
