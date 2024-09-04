import asyncio
import websockets
import json
import httpx


async def send_reload():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:9222/json")

    websocket_url = response.json()[0]["webSocketDebuggerUrl"]

    async with websockets.connect(websocket_url) as websocket:
        await websocket.send(json.dumps({"id": 1, "method": "Page.reload"}))

        response = await websocket.recv()
    print(f"Reload response: {response}")


def run_reload():
    asyncio.run(send_reload())


if __name__ == "__main__":
    run_reload()
