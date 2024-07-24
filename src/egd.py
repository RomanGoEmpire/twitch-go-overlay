import requests

EGD_URL: str = "https://www.europeangodatabase.eu/EGD/GetPlayerDataByData.php"


def players_from_egd(
    last_name: str,
    name: str | None = None,
    country_code: str | None = None,
) -> list[dict]:
    print(last_name)
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
