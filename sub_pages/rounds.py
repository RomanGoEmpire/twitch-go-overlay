from datetime import datetime, time
from pandas._config import options
import streamlit as st
from src.db import DB


# - - - - - FUNCTIONS - - - - -


def string_to_time(time_string: str) -> time:
    hour, minutes = time_string.split("-")
    return time(hour=int(hour), minute=int(minutes))


# - - - - - Page - - - - -
st.header("Rounds")

db: DB = st.session_state["db"]
tournament = st.session_state["active_tournament"]
round = st.session_state["active_round"]
rounds = st.session_state["rounds"]


col1, col2 = st.columns(2)

create_button = col1.button("New Round", type="primary", use_container_width=True)
if create_button:
    db.create("round", data={"tournament": tournament["id"]})
    st.rerun()

delete_button = col2.button("Delete Round", use_container_width=True)
if delete_button:
    db.delete(round["id"])
    st.rerun()

if not rounds:
    st.info(f"No rounds for {tournament["name"]}")
    st.stop()

if not round:
    st.warning("No round selected")
    st.stop()

st.subheader("General")

name = st.text_input("Name", value=round["name"])
col1, col2, col3 = st.columns(3)
date = col1.date_input("Date", value=datetime.fromisoformat(round["date"]))
start = col2.time_input("Start", value=string_to_time(round["start"]))
start_comment = col3.time_input(
    "Start commentary", value=string_to_time(round["start_comment"])
)

commentators = db.sql(
    f"SELECT in.id as person_id,in.name +' ' + in.last_name + ' ' + in.rank  as text from comments where out=={tournament["id"]} "
)
commentators += [{"text": "", "person_id": ""}]


commentator_indexes = [
    next(
        index
        for index, commentator in enumerate(commentators)
        if commentator_round == commentator["person_id"]
    )
    for commentator_round in round["commentators"]
]


selected_commentators = [
    st.selectbox(
        f"Commentator {i+1}",
        commentators,
        commentator_indexes[i],
        format_func=lambda c: c["text"],
    )
    for i in range(4)
]

edited_round = {
    "id": round["id"],
    "active": round["active"],
    "name": name,
    "date": date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "start": start.strftime("%H-%M"),
    "start_comment": start_comment.strftime("%H-%M"),
    "commentators": [c.get("person_id") for c in selected_commentators],
}

if round != edited_round:
    db.update(round["id"], edited_round)

if round["name"] != edited_round["name"]:
    st.rerun()
