import os
import json
import asyncio
from dotenv import load_dotenv
import websockets
from icecream import ic

PATH = "/Users/roman/git/Personal/twitch-go-overlay/overlay"


def update_tournament_files(tournament: dict) -> None:
    ic(tournament)
    open(PATH + "/tournament_name.txt", "w").write(tournament["name"])
    open(PATH + "/tournament_location.txt", "w").write(
        f"{tournament["city"]}, {tournament["country"]}"
    )


def update_commentators(commentators: dict) -> None:
    for index, commentator in enumerate(commentators):
        open(f"{PATH}/commentator{index +1}.txt", "w").write(
            f"{commentator.get("name")} {commentator.get("last_name")} {commentator.get("rank")}"
        )


def update_round_files(round: dict) -> None:
    ic(round)


def update_game_files(game: dict) -> None:
    ic(game)


async def get_result(websocket) -> dict:
    return json.loads(await websocket.recv())["result"]


async def main() -> None:
    load_dotenv()
    os.makedirs("overlay", exist_ok=True)

    uri = os.getenv("SURREAL_URL_WS")

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

    while True:
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(signin_request))
            await websocket.recv()

            await websocket.send(json.dumps(tournament_request))
            tournament_id = json.loads(await websocket.recv())["result"][0]["result"]

            await websocket.send(json.dumps(round_request))
            round_id = json.loads(await websocket.recv())["result"][0]["result"]

            await websocket.send(json.dumps(game_request))
            game_id = json.loads(await websocket.recv())["result"][0]["result"]

            # Listen for live updates

            try:
                while True:
                    update = json.loads(await websocket.recv())["result"]

                    if update["id"] == game_id:
                        update_game_files(update["result"])

                    elif update["id"] == round_id:
                        game_update = await get_result(websocket)
                        update_game_files(game_update["result"])

                        round = update["result"]
                        ic(round)

                        await websocket.send(
                            json.dumps(
                                {
                                    "method": "query",
                                    "params": [
                                        f"select * FROM person WHERE id in {round["commentators"]}"
                                    ],
                                }
                            )
                        )

                        commentators = await get_result(websocket)
                        ic(commentators)
                        update_commentators(commentators[0]["result"])
                        update_round_files(update["result"])

                    if update["id"] == tournament_id:
                        update_tournament_files(update["result"])

            except websockets.exceptions.ConnectionClosed:
                ic("Connection close")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
