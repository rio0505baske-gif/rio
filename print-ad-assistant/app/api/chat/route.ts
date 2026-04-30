import Anthropic from "@anthropic-ai/sdk";
import { SYSTEM_PROMPT } from "@/lib/prompt";

const client = new Anthropic();

export async function POST(req: Request) {
  const { messages } = await req.json();

  const response = await client.messages.create({
    model: "claude-haiku-4-5-20251001",
    max_tokens: 1000,
    system: SYSTEM_PROMPT,
    messages,
  });

  return Response.json({
    content: response.content[0].type === "text" ? response.content[0].text : "",
  });
}
