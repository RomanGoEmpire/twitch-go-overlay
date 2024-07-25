import streamlit as st
from src.db import DB

st.header("Games")

db: DB = st.session_state["db"]
tournament = st.session_state["active_tournament"]
round = st.session_state["active_round"]

if not round:
    st.warning("No rounds")
    st.stop()

games = db.sql(f"SELECT * FROM game WHERE round={round["id"]}")
players = db.sql(
    f"SELECT in.gor, in.* as player, in.name + ' ' + in.last_name + ' ' + in.rank as text from plays where out=={tournament["id"]} order by in.gor DESC"
)

col1, col2 = st.columns(2)

if col1.button("New Game", type="primary", use_container_width=True):
    games += db.create("game", data={"round": round["id"], "game_number": len(games)})

games.sort(key=lambda g: g["game_number"])

for game in games:
    container = st.empty()
    with container:
        with st.expander(game["name"], expanded=False):
            name = st.text_input("Name", game["name"], key=f"{game["id"]}_name")
            col1, col2 = st.columns(2)

            black_index = next(
                (
                    i
                    for i, player in enumerate(players)
                    if player["player"]["id"] == game.get("black_player")
                ),
                0,
            )
            black_player = col1.selectbox(
                "Black player",
                players,
                index=black_index,
                key=f"{game["id"]}_black_player",
                format_func=lambda p: p["text"],
            )
            white_index = next(
                (
                    i
                    for i, player in enumerate(players)
                    if player["player"]["id"] == game.get("white_player")
                ),
                0,
            )
            white_player = col2.selectbox(
                "White player",
                players,
                index=white_index,
                key=f"{game["id"]}_white_player",
                format_func=lambda p: p["text"],
            )
            col1, col2 = st.columns(2, vertical_alignment="bottom")
            ogs_url = col1.text_input(
                "Ogs link", game["ogs_url"], key=f"{game["id"]}_ogs_url"
            )
            col2.link_button("OGS Link", ogs_url, use_container_width=True)
            vdo_ninja_url = st.text_input(
                "VDO Ninja url",
                game["vdo_ninja_url"],
                key=f"{game["id"]}_vdo_ninja_url",
            )
            result = st.text_input("Result", game["result"], key=f"{game["id"]}_result")

            edited_game = {
                "id": game["id"],
                "active": game["active"],
                "name": name,
                "black_player": black_player["player"]["id"],
                "white_player": white_player["player"]["id"],
                "ogs_url": ogs_url,
                "vdo_ninja_url": vdo_ninja_url,
            }

            if game != edited_game:
                db.update(game["id"], data=edited_game)

            if game["name"] != edited_game["name"]:
                st.rerun()

            if st.button("Delete Game", key=f"{game["id"]}_delete"):
                db.delete(game["id"])
                container.empty()


# delete_button = col2.button("Delete Game", use_container_width=True)
# if delete_button:
#     db.delete(game["id"])
#     st.rerun()

if not games:
    st.info(f"There are no games in {tournament["name"]} - {round["name"]}")
    st.stop()
