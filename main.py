import requests
import streamlit as st
from icecream import ic

RULES = {"Japanese", "Chinese", "AGA", "Ing"}
TIME_FORMATS = ["Absolute", "Fischer", "Byo-yomi", "Canadian"]
EGD_CONVERTER_DICT = {
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


# Methods
def person_from_egd(
    last_name: str,
    name: str | None = None,
    country_code: str | None = None,
) -> list[dict]:
    assert len(last_name) >= 2, "The last_name must have at least two letters."

    response: requests.Response = requests.get(
        url="https://www.europeangodatabase.eu/EGD/GetPlayerDataByData.php",
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

    assert type(data.get("players")) == list, "No players in data"
    return [
        {value: person.get(key) for key, value in EGD_CONVERTER_DICT.items()}
        for person in data["players"]
    ]


# App
st.set_page_config(page_title="Twitch Overlay", page_icon="⚫")
st.title("Twitch Overlay")

tournamnets: list = [
    "European Championship 2024",
    "Pandanet 2024",
]  # TODO db call to get tournament


# Session State
persons = []
if "persons" not in st.session_state:
    pass

# Sidebar

with st.sidebar:
    st.selectbox("Tournament", options=tournamnets)


last_name: str = st.text_input(label="Lastname", placeholder="Enter the last name")


if len(last_name) >= 2:
    persons: list[dict] = person_from_egd(last_name)
    persons.sort(key=lambda person: person["gor"], reverse=True)
    st.session_state["persons"] = persons

if persons:
    st.dataframe(persons)
