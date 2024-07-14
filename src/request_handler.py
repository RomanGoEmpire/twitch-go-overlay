from datetime import date
import requests
from icecream import ic

EGD_URL: str = "https://www.europeangodatabase.eu/EGD/GetPlayerDataByData.php"
DB_URL: str = "http://localhost:8000"
DB_URL_SQL: str = f"{DB_URL}/sql"
HEADERS: dict = {"Accept": "application/json", "NS": "test", "DB": "test"}


def people_from_egd(
    last_name: str,
    name: str | None = None,
    country_code: str | None = None,
) -> list[dict]:
    assert last_name, "No last_name provided"
    assert len(last_name) >= 2, "The last_name must have at least two letters."

    response = requests.get(
        url=EGD_URL,
        params={
            "lastname": last_name,
            "name": name,
            "country_code": country_code,
        },
    )
    assert response.status_code == 200, "Error in request to egd"

    data = response.json()

    if data.get("retcode") != "Ok":
        return []
    assert type(data.get("players")) == list, "EGD: No players field in data"

    people = [
        {
            "pin_player": int(person["Pin_Player"]),
            "last_name": person["Last_Name"],
            "name": person["Name"],
            "country_code": person["Country_Code"],
            "club": person["Club"],
            "rank": person["Grade"],
            "gor": int(person["Gor"]),
            "egf_placement": int(person["EGF_Placement"]),
            "total_tournaments": int(person["Tot_Tournaments"]),
        }
        for person in data["players"]
    ]
    people.sort(key=lambda person: person["gor"], reverse=True)
    return people


def db_running() -> bool:
    try:
        requests.get(url=f"{DB_URL}/health")
        return True
    except Exception as e:
        return False


def result_of_response(response: requests.Response) -> list[dict[str, str]]:
    data = response.json()
    assert isinstance(data, list), "response data not a list"
    assert len(data) > 0, "response list has not entries"
    assert "result" in data[0].keys()
    return data[0]["result"]


def get_tournament_names() -> list[dict[str, str]]:
    query: str = "SELECT id,name FROM tournament"
    response = requests.post(url=DB_URL_SQL, headers=HEADERS, data=query)
    assert response.status_code == 200, "error getting tournament names"
    return result_of_response(response)


def get_tournament(id: str) -> dict[str, str]:
    response = requests.get(f"{DB_URL}/key/tournament/{id}", headers=HEADERS)
    assert response.status_code == 200, "error getting tournament"
    return result_of_response(response)[0]


def post_tournament(name: str) -> dict:
    response = requests.post(
        f"{DB_URL}/key/tournament", headers=HEADERS, json={"name": name}
    )
    assert response.status_code == 200, "error getting tournament names"
    return response.json()


def put_tournament(
    name: str,
    country: str | None,
    city: str | None,
    start_date: date | None,
    end_date: date | None,
    rules: str | None,
    time_format: str | None,
    komi: float | None,
    prize_money: str | None,
    sponsor: str | None,
) -> None:
    data = {
        "name": name,
        "country": country,
        "city": city,
        "start_date": start_date,
        "end_date": end_date,
        "rules": rules,
        "time_format": time_format,
        "komi": komi,
        "prize_money": prize_money,
        "sponsor": sponsor,
    }
    response = requests.put(f"{DB_URL}/key/tournament", headers=HEADERS, json=data)
    assert response.status_code == 200, "error getting tournament names"
