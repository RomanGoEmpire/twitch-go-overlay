import streamlit as st
from icecream import ic
from src.db import DB
from surrealdb import SurrealHTTP


db = DB()


st.header("Tournament")

col1, col2 = st.columns(2)
create_button = col1.button(
    "Create Tournament", type="primary", use_container_width=True
)
delete_button = col2.button("Delete Tournament", use_container_width=True)

if create_button:
    # db call to create new
    ic("create")

if delete_button:
    # show confirmation button
    # db call to delete
    ic("delete")
