from icecream.icecream import prefixLinesAfterFirst
import requests
from icecream import ic

URL: str = "https://www.europeangodatabase.eu/EGD/GetPlayerDataByData.php"
PLAYER_REMAPPING_TABLE: dict[str, str] = {
    "Pin_Player": "pin_player",
    "Last_Name": "last_name",
    "Name": "name",
    "Country_Code": "country_code",
    "Club": "club",
    "Grade": "rank",
    "Gor": "gor",
    "EGF_Placement": "egf_placement",
    "Tot_Tournaments": "total_tournaments",
}


def update_player(player: dict) -> dict:
    return {
        PLAYER_REMAPPING_TABLE[key]: value
        for key, value in player.items()
        if key in PLAYER_REMAPPING_TABLE.keys()
    }


def format_players(players: list[dict]) -> list[dict]:
    return list(map(update_player, players))


def get_players_from_egd(
    last_name: str | None = None,
    name: str | None = None,
    country_code: str | None = None,
) -> list[dict]:
    params = {
        "lastname": last_name,
        "name": name,
        "country_code": country_code,
    }
    response: requests.Response = requests.get(URL, params=params)
    data = response.json()

    assert response.status_code == 200, "Error in request to egd"
    if data.get("retcode") == "Ok":
        assert type(data.get("players")) == list, "No players in data"
        players: list = data["players"]
        formatted_players = format_players(players)
        return formatted_players
    return []


if __name__ == "__main__":
    ic(get_players_from_egd(last_name="xxx"))
