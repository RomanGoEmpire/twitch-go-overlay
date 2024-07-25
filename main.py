import streamlit as st

from src.db import DB

st.title("Twitch Go Overlay")

db = DB()
st.session_state["db"] = db

with st.sidebar:
    tournaments = db.select("tournament")
    st.session_state["tournaments"] = tournaments

    active_tournament = st.selectbox(
        "Tournament",
        options=tournaments,
        format_func=lambda t: t["name"],
        key="active_tournament",
    )

    rounds = db.sql(f"SELECT * FROM round WHERE tournament== {active_tournament["id"]}")
    st.session_state["rounds"] = rounds

    active_round = st.selectbox(
        "Round",
        options=rounds,
        format_func=lambda t: t["name"],
        key="active_round",
    )


if "players" not in st.session_state:
    st.session_state["players"] = db.sql(
        f"SELECT id, name +' ' + last_name + ' ' + rank  as text, gor from person  order by gor DESC"
    )


pages = {
    "Planning": [
        st.Page("sub_pages/people.py", title="People", icon=":material/people:"),
        st.Page(
            "sub_pages/tournaments.py",
            title="Tournament",
            icon=":material/emoji_events:",
        ),
        st.Page(
            "sub_pages/rounds.py", title="Rounds", icon=":material/calendar_today:"
        ),
        st.Page("sub_pages/games.py", title="Games", icon=":material/hdr_weak:"),
    ],
    "Live": [st.Page("sub_pages/live.py", title="On Air", icon=":material/live_tv:")],
}


pg = st.navigation(pages)
pg.run()
