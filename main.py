import streamlit as st

from src.db import DB

st.title("Twitch Go Overlay")

db = DB()
st.session_state["db"] = db

with st.sidebar:
    tournaments = db.select("tournament")

    active_tournament = st.selectbox(
        "Tournament",
        options=tournaments,
        format_func=lambda t: t["name"],
        key="active_tournament",
    )


pages = {
    "Plan": [
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
    "Live": [st.Page("sub_pages/live.py", title="On Air")],
}


pg = st.navigation(pages)
pg.run()
