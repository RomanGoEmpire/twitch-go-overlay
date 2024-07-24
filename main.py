import streamlit as st

st.title("Twitch Go Overlay")

pages = {
    "Plan": [
        st.Page("sub_pages/tournaments.py", title="Tournament"),
        st.Page("sub_pages/rounds.py", title="Rounds"),
        st.Page("sub_pages/games.py", title="Games"),
    ],
    "Live": [st.Page("sub_pages/live.py", title="On Air")],
}

with st.sidebar:
    tournaments = ["European Championship 2024", "European Championship 2025"]
    db_active_tournament = "European Championship 2024"
    tournament_index = tournaments.index(db_active_tournament)
    active_tournament = st.selectbox(
        "Active Tournament",
        options=tournaments,
        index=tournament_index,
        key="active_tournament",
    )
    if db_active_tournament != active_tournament:
        # TODO update db active tournament
        pass

    # TODO get rounds from DB and get active index
    rounds = ["Round 1", "Round 2"]
    db_active_round = "Round 2"
    round_index = rounds.index(db_active_round)
    active_round = st.selectbox(
        "Active Round", options=rounds, index=round_index, key="active_round"
    )
    if db_active_round != active_round:
        # Todo update active round
        pass


pg = st.navigation(pages)
pg.run()
