import os

import requests
from dotenv import load_dotenv

load_dotenv()


class SellsyClient:
    AUTH_URL = "https://login.sellsy.com/oauth2/access-tokens"
    CONTACT_API_URL = "https://api.sellsy.com/v2/contacts"

    def __init__(self):
        self.token = self.authenticate()

    def authenticate(self):
        response = requests.post(
            self.AUTH_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": os.getenv("SELLSY_CLIENT_ID"),
                "client_secret": os.getenv("SELLSY_CLIENT_SECRET"),
            },
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def push_contact(self, contact):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(self.CONTACT_API_URL, json=contact, headers=headers)
        response.raise_for_status()
        return response.json()
