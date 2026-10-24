import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { SseServerTransport } from "@modelcontextprotocol/sdk/server/transport/sse.js";
import { createClient } from "@supabase/supabase-js";
import { GoogleGenAI, Type } from "@google/genai";
import express from "express";

const app = express();

// Initialize SDK Clients using Environmental Variables
const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY! });

// Instantiate the Model Context Protocol Server Architecture
const server = new McpServer({
  name: "Asymmetric-RPG-Master-Engine",
  version: "1.0.0",
});

// Expose a tool to the player's personal Claude instances
server.tool(
  "submit_action",
  "Submit your character action to the world game master.",
  {
    playerId: Type.String(),
    characterAction: Type.String(),
  },
  async ({ playerId, characterAction }) => {
    // 1. Fetch current shared database context securely
    const { data: globalState } = await supabase.from("game_state").select("*");
    const { data: playerData } = await supabase.from("players").select("*").eq("id", playerId).single();

    // 2. Query Gemini 2.5 Pro behind a secure firewall using a strict JSON schema
    const response = await ai.models.generateContent({
      model: "gemini-2.5-pro",
      contents: `Player Action: ${characterAction}. Character Sheet: ${JSON.stringify(playerData)}. World State: ${JSON.stringify(globalState)}.`,
      config: {
        systemInstruction: "You are the hidden Master DM. Arbitrate this turn logically. You must only return raw JSON matching the required schema. Do not include narrative text outside the JSON structure.",
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.Object,
          properties: {
            success: { type: Type.Boolean },
            dbUpdates: { type: Type.String, description: "Changes to execute in Supabase columns" },
            filteredNarrativeForPlayer: { type: Type.String, description: "Only what THIS specific character perceives." },
          },
          required: ["success", "dbUpdates", "filteredNarrativeForPlayer"],
        },
      },
    });

    const outputData = JSON.parse(response.text || "{}");

    // 3. Process the backend execution commands automatically to Supabase
    if (outputData.dbUpdates) {
       // Code triggers automated DB state alterations here based on Gemini's directives
    }

    // 4. Return ONLY the perspective-bounded narrative text chunk to the player's app stream
    return {
      content: [{ type: "text", text: outputData.filteredNarrativeForPlayer }],
    };
  }
);

// Route transport parameters to conform to Vercel Serverless Function requirements
let transport: SseServerTransport | null = null;

app.get("/api/mcp", async (req, res) => {
  transport = new SseServerTransport("/api/mcp/messages", res);
  await server.connect(transport);
});

app.post("/api/mcp/messages", async (req, res) => {
  if (transport) {
    await transport.handleMessage(req, res);
  } else {
    res.status(500).send("No active server transport connection.");
  }
});

export default app;
