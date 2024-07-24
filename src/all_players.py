import os
import json
import asyncio
from icecream import ic

from egd import players_from_egd
from surrealdb import Surreal
from dotenv import load_dotenv

load_dotenv()

letters = "abcdefghijklmnopqrstuvwxyz"
combinations = [letter1 + letter2 for letter1 in letters for letter2 in letters]

ids = []
all_players = []

for index, name in enumerate(combinations):
    if index % 10 == 0:
        ic(index)
    players = players_from_egd(last_name=name)
    for player in players:
        if player["pin_player"] not in ids:
            ids.append(player["pin_player"])
            all_players.append(player)


with open("output.json", "w") as f:
    json.dump(all_players, f, indent=4)


load_dotenv()

URL = os.getenv("SURREAL_URL")
USER = os.getenv("SURREAL_USER")
PASSWORD = os.getenv("SURREAL_PASSWORD")


async def upload_players():
    all_players = json.load(open("players.json", "r"))
    db = Surreal(url=URL)
    await db.connect()
    await db.signin({"user": USER, "pass": PASSWORD})
    await db.use("main", "main")

    for index, player in enumerate(all_players):
        if index % 1000 == 0:
            ic(index)
        try:
            await db.create(f"person:{player['pin_player']}", data=player)
        except Exception as e:
            pass


asyncio.run(upload_players())
