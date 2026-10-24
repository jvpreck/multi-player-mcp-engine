import { createMcpHandler } from 'mcp-handler';
import { createClient } from '@supabase/supabase-js';
import { GoogleGenAI, Type } from '@google/genai';
import { z } from 'zod';

// Initialize SDK Clients behind the scenes
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const handler = createMcpHandler((server) => {
  // Register your action submitter tool using Vercel's native schema compiler
  server.registerTool(
    'submit_action',
    {
      description: 'Submit your character action to the world game master.',
      inputSchema: z.object({
        playerId: z.string(),
        characterAction: z.string()
      }),
    },
    async ({ playerId, characterAction }) => {
      // 1. Pull data records from Supabase
      const { data: globalState } = await supabase.from('game_state').select('*');
      const { data: playerData } = await supabase.from('players').select('*').eq('id', playerId).single();

      // 2. Compute logic through Gemini 3.5 Flash Lite
      const response = await ai.models.generateContent({
        model: 'gemini-3.5-flash-lite',
        contents: `Player: ${playerId}. Action: ${characterAction}. Sheet: ${JSON.stringify(playerData)}. State: ${JSON.stringify(globalState)}`,
        config: {
          systemInstruction: "You are a backend RPG data referee. Do not write creative narratives. Determine the mechanical outcome and output hidden facts that their character can visibly discover. Keep 'visibleFactsForPlayer' concise and factual.",
          responseMimeType: 'application/json',
          responseSchema: {
            type: Type.Object,
            properties: {
              success: { type: Type.Boolean },
              supabasePayload: { type: Type.String },
              visibleFactsForPlayer: { type: Type.String }
            },
            required: ['success', 'supabasePayload', 'visibleFactsForPlayer']
          }
        }
      });

      const outputData = JSON.parse(response.text || '{}');

      // 3. Optional: Add your custom automated Supabase mutations here

      // 4. Return synthetic facts package directly to the local Claude app
      return {
        content: [{ type: 'text', text: outputData.visibleFactsForPlayer || "Action evaluated." }],
      };
    },
  );
});

// Export standard handlers required by Vercel Functions natively
export { handler as GET, handler as POST };
