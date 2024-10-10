import requests
import os

class PermitService:
    BASE_URL = "https://api.permit.io/v2"

    def __init__(self):
        self.api_key = os.getenv("PERMIT_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_resources(self):
        response = requests.get(f"{self.BASE_URL}/resources", headers=self.headers)
        return response.json()

    def get_roles(self):
        response = requests.get(f"{self.BASE_URL}/roles", headers=self.headers)
        return response.json()

    def get_relationships(self):
        response = requests.get(f"{self.BASE_URL}/relationships", headers=self.headers)
        return response.json()
