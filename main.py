from datetime import date, timedelta
import datetime
from decimal import DecimalException
from pandas._libs.tslibs.np_datetime import py_td64_to_tdstruct
import requests
import streamlit as st
from icecream import ic
import pycountry
from streamlit.commands.navigation import pages_from_nav_sections

from src.request_handler import (
    get_tournament_names,
    get_tournament,
    people_from_egd,
    post_tournament,
    db_running,
    put_tournament,
)

# ToDo Change it to other url


COUNTRIES = [c.name for c in pycountry.countries]
RULES: list = ["Japanese", "Chinese", "AGA", "Ing"]
TIME_FORMATS: list = ["Absolute", "Fischer", "Byo-yomi", "Canadian"]


# Methods
@st.experimental_dialog("New Tournament")
def dialog_new_tournament() -> None:
    tournament_name = st.text_input(
        "Tournament name", placeholder="Tournament name", key="tournament_name"
    )
    if tournament_name in tournament_names:
        st.error("Tournament name exists")
    if st.button(
        "Submit", disabled=tournament_name in tournament_names, type="primary"
    ):
        post_tournament(tournament_name)
        st.session_state.new_tournament = tournament_name
        st.rerun()


# App
st.set_page_config(page_title="Twitch Overlay", page_icon="⚫")
st.title("Twitch Overlay")

if not db_running():
    st.error("Database is not running", icon=":material/cloud_off:")
    st.stop()

# Variables and Session State

tournaments = get_tournament_names()
tournament_names = [tournament.get("name") for tournament in tournaments]


# Sidebar

with st.sidebar:
    st.subheader("Tournaments")
    if st.button("New Tournament", type="primary"):
        dialog_new_tournament()

    if not tournaments:
        st.info("There are no Tournaments")
        st.stop()

    selected_tournament_name = st.selectbox(
        "Tournament", options=tournament_names, key="selected_tournament"
    )

    if "new_tournament" in st.session_state:
        st.success(
            f"Added {st.session_state["new_tournament"]}", icon=":material/done:"
        )
        del st.session_state["new_tournament"]


tournament_id = next(
    (t["id"] for t in tournaments if t["name"] == selected_tournament_name)
)
tournament_data: dict = get_tournament(tournament_id)
with st.expander(str(selected_tournament_name), expanded=True):
    new_name = st.text_input("Tournament name", selected_tournament_name)
    country = st.selectbox(
        "Country",
        options=COUNTRIES,
        index=COUNTRIES.index(tournament_data.get("country", "Angola")),
    )
    city = st.text_input("City", tournament_data.get("city", ""))

    if "start_date" in tournament_data and "end_date" in tournament_data:
        dates_values = [
            datetime.datetime.strptime(tournament_data["start_date"], "%Y-%m-%d"),
            datetime.datetime.strptime(tournament_data["end_date"], "%Y-%m-%d"),
        ]
    else:
        dates_values = [date.today(), date.today()]
    tournament_dates = st.date_input("Dates", dates_values)

    rules = st.selectbox(
        "Rules",
        options=RULES,
        index=RULES.index(tournament_data.get("rules", "Japanese")),
    )

    time_format = st.selectbox(
        "Time control",
        options=TIME_FORMATS,
        index=TIME_FORMATS.index(tournament_data.get("time_format", "Fischer")),
    )
    komi = st.number_input(
        "Komi", value=tournament_data.get("komi", 6.5), format="%1.f"
    )
    prize_money = st.text_area(
        "Prize money", value=tournament_data.get("prize_money", "")
    )
    sponsor = st.text_area("Sponsor", value=tournament_data.get("sponsor", ""))

    if st.button(
        "Update Tournament",
    ):
        put_tournament(
            str(new_name),
            country,
            city,
            tournament_dates[0].isoformat(),
            tournament_dates[1].isoformat(),
            rules,
            time_format,
            komi,
            prize_money,
            sponsor,
        )
        st.session_state.updated_tournament = f"Updated {new_name}"
        st.rerun()
    if st.button("Delete Tournament"):
        # TODO add delete function
        pass

if st.session_state.get("updated_tournament"):
    st.success(st.session_state.get("updated_tournament"), icon=":material/done:")
    del st.session_state["updated_tournament"]
# col1, col2 = st.columns(2)
# last_name: str = col1.text_input(label="Lastname", placeholder="Enter last name")
# name: str = col2.text_input("Name", placeholder="Enter name")
#
# if len(last_name) >= 2:
#     people: list[dict] = people_from_egd(last_name, name)
#     st.dataframe(people)
# else:
#     st.warning("Lastname has to have atleast 2 characters")
