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
tournament = st.session_state["active_tournament"]
tournaments = st.session_state["tournaments"]


col1, col2 = st.columns(2)

create_button = col1.button("New Tournament", type="primary", use_container_width=True)
if create_button:
    db.create("tournament")
    st.rerun()

delete_button = col2.button("Delete Tournament", use_container_width=True)
if delete_button:
    db.delete(tournament["id"])
    st.rerun()

if not tournaments:
    st.info("No Tournament")
    st.stop()

st.subheader("General")
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
    "time_settings": time_settings.strip(),
    "rules": rules,
    "komi": komi,
}


if tournament != edited_tournament:
    db.update(tournament["id"], edited_tournament)

if tournament["name"] != edited_tournament["name"]:
    st.rerun()


st.subheader("Players")
col1, col2 = st.columns([0.7, 0.3], vertical_alignment="bottom")
selected_player = col1.selectbox(
    "Add Player", options=st.session_state["players"], format_func=lambda p: p["text"]
)
if col2.button("Add player", type="primary", use_container_width=True):
    is_already_player = db.sql(
        f"select * from plays where in=={selected_player["id"]} and out=={tournament["id"]}"
    )
    if not is_already_player:
        db.sql(f"RELATE {selected_player["id"]}->plays->{tournament["id"]}")


player_in_tournament = [
    player["player"]
    for player in db.sql(
        f"SELECT in.gor, in.* as player from plays where out=={tournament["id"]} order by in.gor DESC"
    )
]
st.info(f"Total Players: {len(player_in_tournament)}")

with st.expander("Players", expanded=True):
    st.dataframe(
        data=player_in_tournament,
        column_order=[
            "name",
            "last_name",
            "rank",
            "gor",
            "egf_placement",
            "country_code",
            "club",
            "total_tournaments",
        ],
        use_container_width=True,
    )

st.subheader("Commentators")

col1, col2 = st.columns([0.7, 0.3], vertical_alignment="bottom")
selected_commentator = col1.selectbox(
    "Add Commentator",
    options=st.session_state["players"],
    format_func=lambda p: p["text"],
)
if col2.button("Add Commentator", type="primary", use_container_width=True):
    is_already_player = db.sql(
        f"select * from comments where in=={selected_commentator["id"]} and out=={tournament["id"]}"
    )
    if not is_already_player:
        db.sql(f"RELATE {selected_commentator["id"]}->comments->{tournament["id"]}")

commentators_in_tournament = [
    player["player"]
    for player in db.sql(
        f"SELECT in.gor, in.* as player from comments where out=={tournament["id"]} order by in.gor DESC"
    )
]
with st.expander("Commentators", expanded=True):
    st.dataframe(
        data=commentators_in_tournament,
        column_order=[
            "name",
            "last_name",
            "rank",
            "gor",
            "egf_placement",
            "country_code",
            "club",
            "total_tournaments",
        ],
        use_container_width=True,
    )
