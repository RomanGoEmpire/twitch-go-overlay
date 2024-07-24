import os
import json
import requests
from requests import Response
from icecream import ic
from dotenv import load_dotenv
from streamlit.elements.map import Data


load_dotenv()
URL = os.getenv("SURREAL_URL")
HEADERS = {"Accept": "application/json", "DB": "main", "NS": "main"}
AUTH = os.getenv("SURREAL_USER"), os.getenv("SURREAL_PASSWORD")


class DB:

    def select(self, table: str, id: str | int | None = None) -> list[dict]:
        response = requests.get(url=url(table, id), headers=HEADERS, auth=AUTH)
        return extract(response)

    def create(
        self, table: str, id: str | int | None = None, data: dict = {}
    ) -> list[dict]:

        response = requests.post(
            url=url(table, id),
            headers=HEADERS,
            auth=AUTH,
            json=data,
        )
        return extract(response)

    def update(
        self, table: str, id: str | int | None = None, data: dict = {}
    ) -> list[dict]:
        response = requests.patch(
            url=url(table, id),
            headers=HEADERS,
            auth=AUTH,
            json=data,
        )
        return extract(response)

    def delete(
        self, table: str, id: str | int | None = None, data: dict = {}
    ) -> list[dict]:
        response = requests.delete(
            url=url(table, id),
            headers=HEADERS,
            auth=AUTH,
        )
        return extract(response)

    def sql(self, query: str) -> list[dict]:
        response = requests.post(
            url=f"{URL}/sql", headers=HEADERS, auth=AUTH, data=query
        )
        return extract(response)


def url(table: str, id: str | int | None) -> str:
    return f"{URL}/key/{table}/{id}" if id else f"{URL}/key/{table}"


def extract(response) -> list[dict]:
    return json.loads(response.content.decode())[0]["result"]
