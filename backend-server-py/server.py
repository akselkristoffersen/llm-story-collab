import os
import asyncio
import websockets
import torch
from transformers import pipeline

model_name = os.environ["AX_MODEL_NAME"]

generator = pipeline(
    "text-generation",
    model=model_name,
    tokenizer=model_name,
    model_kwargs={"torch_dtype": torch.float16},
    device_map="auto"
)

generator_lock = asyncio.Lock()

async def run_inference(monologue):
    loop = asyncio.get_event_loop()
    async with generator_lock:
        monologue = await loop.run_in_executor(None, lambda : generator(
                    monologue,
                    max_new_tokens=5,
                    num_return_sequences=1,
                    do_sample=False,
                    truncation=True,
                    pad_token_id = generator.tokenizer.eos_token_id
                )[0]['generated_text'])
    return monologue

async def echo(websocket, path):
    monologue = ""
    async for client_contribution in websocket:
        monologue += client_contribution
        monologue_size = len(monologue)
        monologue = await run_inference(monologue)
        await websocket.send(monologue[monologue_size:])

async def main():
    async with websockets.serve(echo, "", 8080):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())