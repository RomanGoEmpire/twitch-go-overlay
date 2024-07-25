import streamlit as st
from src.db import DB

st.header("Live")

db: DB = st.session_state["db"]
tournament = st.session_state["active_tournament"]
round = st.session_state["active_round"]
games = db.sql(f"SELECT * FROM game WHERE round={round["id"]} order by game_number")

st.subheader(tournament["name"])
tournament
round
games
