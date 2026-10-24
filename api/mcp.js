import { createMcpHandler } from 'mcp-handler';
import { createClient } from '@supabase/supabase-js';
import { GoogleGenerativeAI } from '@google/generative-ai'; // Adjusted name here
import { z } from 'zod';

// Initialize SDK Clients using Environmental Variables
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);
const ai = new GoogleGenerativeAI(process.env.GEMINI_API_KEY); // Adjusted constructor name here

const handler = createMcpHandler((server) => {
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

      // 2. Compute logic through the stable Gemini client
      const model = ai.getGenerativeModel({
        model: 'gemini-3.5-flash-lite',
        generationConfig: {
          responseMimeType: 'application/json',
        }
      });

      const prompt = `
        Player ID: ${playerId}
        Character Action: ${characterAction}
        Character Sheet: ${JSON.stringify(playerData)}
        World State: ${JSON.stringify(globalState)}
      `;

      const model = genAI.getGenerativeModel({
        model: "gemini-3.5-flash-lite",
        systemInstruction:
          "You are a backend RPG data referee. Do not write creative narratives. Determine the mechanical outcome and output hidden facts that their character can visibly discover. You must return a valid JSON object with the properties: success (boolean), supabasePayload (string), and visibleFactsForPlayer (string).",
        generationConfig: { responseMimeType: "application/json" },
      });
      
      const response = await model.generateContent({
        contents: [{ role: "user", parts: [{ text: prompt }] }],
      });
      
      const outputData = JSON.parse(response.response.text() || '{}');
            
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
