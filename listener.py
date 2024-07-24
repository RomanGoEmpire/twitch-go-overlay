import os
import json
import asyncio
import websockets
from icecream import ic


async def main() -> None:

    uri = os.getenv("SURREAL_URL_WS")

    async with websockets.connect(uri) as websocket:
        # Sign in
        signin_request = {
            "method": "signin",
            "params": [
                {
                    "user": os.getenv("SURREAL_USER"),
                    "pass": os.getenv("SURREAL_PASSWORD"),
                    "db": "main",
                    "ns": "main",
                }
            ],
        }
        await websocket.send(json.dumps(signin_request))
        await websocket.recv()

        info_request = {"method": "live", "params": ["test"]}
        person_request = {"method": "live", "params": ["person"]}

        await websocket.send(json.dumps(info_request))
        await websocket.recv()
        await websocket.send(json.dumps(person_request))
        await websocket.recv()

        # Listen for live updates
        try:
            while True:
                message = await websocket.recv()
                print(f"Live Update: {message}")

        except websockets.exceptions.ConnectionClosed:
            ic("Connection closed")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
