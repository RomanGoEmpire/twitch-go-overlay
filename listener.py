import os
import json
import asyncio
from dotenv import load_dotenv
import websockets
from icecream import ic


def update_tournament_files(tournament: dict) -> None:
    ic("tournament")


def update_round_files(round: dict) -> None:
    ic("round")


def update_game_files(game: dict) -> None:
    ic("game")


async def main() -> None:
    load_dotenv()

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

        tournament_request = {
            "method": "query",
            "params": ["LIVE SELECT * FROM tournament WHERE active=true"],
        }
        round_request = {
            "method": "query",
            "params": ["LIVE SELECT * FROM round WHERE active=true"],
        }
        game_request = {
            "method": "query",
            "params": ["LIVE SELECT * FROM game WHERE active=true"],
        }

        await websocket.send(json.dumps(tournament_request))
        tournament_id = json.loads(await websocket.recv())["result"][0]["result"]

        await websocket.send(json.dumps(round_request))
        round_id = json.loads(await websocket.recv())["result"][0]["result"]

        await websocket.send(json.dumps(game_request))
        game_id = json.loads(await websocket.recv())["result"][0]["result"]

        # Listen for live updates
        try:
            while True:
                update = await websocket.recv()
                update = json.loads(update)
                update = update["result"]
                ic(tournament_id, round_id, game_id)
                ic(update)
                if update["id"] == tournament_id:
                    update_tournament_files(update["result"])
                elif update["id"] == round_id:
                    update_round_files(update["result"])
                elif update["id"] == game_id:
                    update_game_files(update["result"])

        except websockets.exceptions.ConnectionClosed:
            ic("Connection closed")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
