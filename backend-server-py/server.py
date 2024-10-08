import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "", 8080):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())