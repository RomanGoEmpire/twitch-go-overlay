from datetime import datetime
import pycountry
import streamlit as st

from src.db import DB

# - - - - - CONSTANTS - - - - -
RULES = ["Japanese", "Chinese", "AGA", "ING"]
TIME_FORMAT = ["Byo-yomi", "Fischer", "Canadian", "Absolute"]
COUNTRIES = [c.name for c in pycountry.countries]
# - - - - - PAGE - - - - -

st.header("Tournament")

db: DB = st.session_state["db"]

tournaments = db.select("tournament")

if not tournaments:
    st.stop()

tournament = st.session_state["active_tournament"]
assert type(tournament) == dict, "Selected tournament is not a dict"

name = st.text_input("Name", tournament["name"])

col1, col2 = st.columns(2)

city = col1.text_input("City", tournament["city"])
country = col2.selectbox(
    "Country",
    COUNTRIES,
    (
        COUNTRIES.index(tournament["country"])
        if tournament["country"] in COUNTRIES
        else 0
    ),
)
start_date = col1.date_input(
    "Start date", datetime.fromisoformat(tournament["start_date"])
)
end_date = col2.date_input("End date", datetime.fromisoformat(tournament["end_date"]))
time_format = col1.selectbox(
    "Time format",
    TIME_FORMAT,
    TIME_FORMAT.index(tournament["time_format"]),
)
time_settings = col2.text_input("Time settings", tournament["time_settings"])
rules = col1.selectbox("Rules", RULES, RULES.index(tournament["rules"]))
komi = col2.number_input("Komi", value=tournament["komi"], format="%.1f")


edited_tournament = {
    "id": tournament["id"],
    "active": tournament["active"],
    "name": name.strip(),
    "city": city.strip(),
    "country": country,
    "start_date": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "end_date": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "time_format": time_format,
    "time_settings": time_settings,
    "rules": rules,
    "komi": komi,
}


if tournament != edited_tournament:
    db.update(tournament["id"], edited_tournament)

if tournament["name"] != edited_tournament["name"]:
    st.rerun()


create_button = st.button("New Tournament", type="primary", use_container_width=True)
if create_button:
    db.create("tournament")
    st.rerun()

delete_button = st.button("Delete Tournament", use_container_width=True)
if delete_button:
    db.delete(tournament["id"])
    st.rerun()
