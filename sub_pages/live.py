import streamlit as st
from src.db import DB

st.header("Live")

db: DB = st.session_state["db"]
tournament = st.session_state["active_tournament"]
round = st.session_state["active_round"]
games = db.sql(
    f"""SELECT *,
    black_player.name + ' ' + black_player.last_name + ' ' +  black_player.rank as black_player,
    white_player.name + ' ' + white_player.last_name + ' ' +  white_player.rank as white_player
    FROM game
    WHERE round={round["id"]} order by game_number"""
)


for game in games:
    if st.button(
        f"{game["name"]} - {game["black_player"]} vs {game["white_player"]}",
        type="primary" if game["active"] else "secondary",
        use_container_width=True,
    ):
        db.sql(f"UPDATE game set active=False WHERE round=={round["id"]}")
        db.update(game["id"], data={"active": True})
        st.rerun()
