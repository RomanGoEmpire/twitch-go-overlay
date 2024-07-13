import requests
import streamlit as st
from icecream import ic
import pycountry

EGD_URL: str = "https://www.europeangodatabase.eu/EGD/GetPlayerDataByData.php"
# ToDo Change it to other url
DB_URL: str = "http://localhost:8000"
HEADERS: dict = {
    "NS": "test",
    "DB": "test",
    "Accept": "application/json",
}

COUNTRIES = {c.name: c.alpha_2 for c in pycountry.countries}
RULES: list = ["Japanese", "Chinese", "AGA", "Ing"]
TIME_FORMATS: list = ["Absolute", "Fischer", "Byo-yomi", "Canadian"]


# Methods
def people_from_egd(
    last_name: str,
    name: str | None = None,
    country_code: str | None = None,
) -> list[dict]:
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


def result_of_response(response: requests.Response) -> list[dict]:
    return response.json()[0]["result"]


def get_tournaments() -> list[dict]:
    response = requests.get(url=f"{DB_URL}/key/tournament", headers=HEADERS)
    assert response.status_code == 200, "error getting tournament names"
    return result_of_response(response)


# Dialog


@st.experimental_dialog("Add Tournament")
def add_tournament_dialog() -> None:

    tournament_name = st.text_input(
        "Tournament name", placeholder="Enter Tournament name"
    )
    # TODO add all fields to
    # country = st.selectbox("Country", options=[c.name for c in pycountry.countries])

    if st.button("Submit"):
        response = requests.post(
            f"{DB_URL}/key/tournament", headers=HEADERS, json={"name": tournament_name}
        )
        st.session_state.new_tournament = tournament_name
        st.rerun()


# App
st.set_page_config(page_title="Twitch Overlay", page_icon="⚫")
st.title("Twitch Overlay")


# Variables and Session State

people = []
tournaments = []
if "tournaments" not in st.session_state:
    tournaments = get_tournaments()
    st.session_state["tournamnets"] = tournaments

# Sidebar

with st.sidebar:
    st.subheader("Tournaments")
    st.selectbox(
        "Tournament", options=[tournament["name"] for tournament in tournaments]
    )

    if "new_tournament" not in st.session_state:
        if st.button("Add Tournament", type="primary"):
            add_tournament_dialog()
    else:
        st.success(
            f"Added {st.session_state["new_tournament"]}", icon=":material/done:"
        )
        del st.session_state["new_tournament"]

col1, col2 = st.columns(2)
last_name: str = col1.text_input(label="Lastname", placeholder="Enter last name")
name: str = col2.text_input("Name", placeholder="Enter name")

if len(last_name) >= 2:
    people: list[dict] = people_from_egd(last_name, name)
    st.session_state["people"] = people
else:
    st.warning("Lastname has to have atleast 2 characters")

if people:
    st.dataframe(people)
