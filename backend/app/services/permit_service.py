from fastapi import APIRouter, Depends, HTTPException
import requests
import os

router = APIRouter()

class PermitService:
    BASE_URL = "https://api.permit.io/v2"

    def __init__(self):
        self.api_key = os.getenv("PERMIT_API_KEY")
        if not self.api_key:
            raise ValueError("PERMIT_API_KEY not set in environment")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(self, endpoint: str):
        try:
            response = requests.get(f"{self.BASE_URL}/{endpoint}", headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=response.status_code, detail=f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as err:
            raise HTTPException(status_code=500, detail=f"Error occurred while connecting to Permit API: {err}")

    def get_resources(self):
        return self._make_request("resources")

    def get_roles(self):
        return self._make_request("roles")

    def get_relationships(self):
        return self._make_request("relationships")

permit_service = PermitService()

@router.get("/roles")
def read_roles():
    return permit_service.get_roles()
