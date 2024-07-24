import os
import json
import requests
from requests import Response
from icecream import ic
from dotenv import load_dotenv
from streamlit.elements.map import Data


class DB:

    def __init__(self) -> None:
        load_dotenv()
        self.URL = os.getenv("SURREAL_URL")
        self.headers = {"Accept": "application/json", "DB": "main", "NS": "main"}
        self.auth = os.getenv("SURREAL_USER"), os.getenv("SURREAL_PASSWORD")

    def select(self, key: str) -> list[dict]:
        response = requests.get(url=self.url(key), headers=self.headers, auth=self.auth)
        return extract(response)

    def create(self, key: str, data: dict = {}) -> list[dict]:

        response = requests.post(
            url=self.url(key),
            headers=self.headers,
            auth=self.auth,
            json=data,
        )
        return extract(response)

    def update(self, key: str, data: dict = {}) -> list[dict]:
        response = requests.patch(
            url=self.url(key),
            headers=self.headers,
            auth=self.auth,
            json=data,
        )
        return extract(response)

    def delete(self, key: str, data: dict = {}) -> list[dict]:
        response = requests.delete(
            url=self.url(key),
            headers=self.headers,
            auth=self.auth,
        )
        return extract(response)

    def sql(self, query: str) -> list[dict]:
        response = requests.post(
            url=f"{self.URL}/sql", headers=self.headers, auth=self.auth, data=query
        )
        return extract(response)

    def url(self, key: str) -> str:
        if ":" in key:
            table, id = key.split(":")
            return f"{self.URL}/key/{table}/{id}"
        else:
            return f"{self.URL}/key/{key}"

    def active_tournament(self, key: str) -> None:
        self.update("tournament", data={"active": False})
        self.update(key, data={"active": True})


def extract(response) -> list[dict]:
    return json.loads(response.content.decode())[0]["result"]
