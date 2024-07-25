import streamlit as st
from src.db import DB

st.header("Live")

db: DB = st.session_state["db"]
tournaments = db.select("tournament")

if not tournaments:
    st.write("No tournaments")
    st.stop()

active_tournament = st.selectbox(
    "Active round",
    tournaments,
    index=next(
        (i for i, tournament in enumerate(tournaments) if tournament["active"]), 0
    ),
    format_func=lambda t: t["name"],
)
if not active_tournament["active"]:
    db.sql("UPDATE tournament set active=False")
    db.update(active_tournament["id"], data={"active": True})
    st.rerun()

rounds = db.sql(f"SELECT * FROM round WHERE tournament=={active_tournament["id"]}")

if not rounds:
    st.error("No rounds")
    st.stop()

active_round = st.selectbox(
    "Active round",
    rounds,
    index=next((i for i, round in enumerate(rounds) if round["active"]), 0),
    format_func=lambda r: r["name"],
)

if not active_round["active"]:
    db.sql("UPDATE round set active=False")
    db.update(active_round["id"], data={"active": True})
    st.rerun()

games = db.sql(
    f"""SELECT *,
    black_player.name + ' ' + black_player.last_name + ' ' +  black_player.rank as black_player,
    white_player.name + ' ' + white_player.last_name + ' ' +  white_player.rank as white_player
    FROM game
    WHERE round={active_round["id"]} order by game_number"""
)

active_game = st.selectbox(
    "Active Game",
    games,
    index=next((i for i, game in enumerate(games) if game["active"]), 0),
    format_func=lambda g: f"{g["name"]} - {g["black_player"]} vs {g["white_player"]}",
)

if not active_game["active"]:
    db.sql(f"UPDATE game set active=False WHERE round=={active_round["id"]}")
    db.update(active_game["id"], data={"active": True})
    st.rerun()
