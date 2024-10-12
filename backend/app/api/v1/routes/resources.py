from fastapi import APIRouter, Depends
from dependencies.permission_checker import Enforcer
from services.permit_service import PermitService
import httpx
import os

router = APIRouter()
permit_service = PermitService()

PERMIT_API_URL = "http://permit-pdp:7000"

from permit import Permit

permit = Permit(
      pdp=PERMIT_API_URL,
      token=os.getenv("PERMIT_API_KEY"),
  )

headers = {
    "Authorization": "Bearer permit_key_C0inu72bDJzvUVwrCwbSPvAN36CPMheDMHvxmbXAapq0PrjMuuzX8qZbWpokoiPoMzpIEijBSd55V1N53moHIm",
    "Content-Type": "application/json"
}


@router.get("/")
def read_resources():
    return permit_service.get_resources()

@router.get("/read-document")
async def read_repository(
    permission_check: Depends = Depends(
        Enforcer(
            resource_key="repository",
            action_name="read",
            context={"additional": "context_info"}
        )
    )
):
    
    return {"message": "You have access to this "}


rebac_data = [
    {"resourceType": "repository", "resource": "repository", "role": "owner", "actions": ["create", "delete", "read", "update"]},
    {"resourceType": "repository", "resource": "repository", "role": "collaborator", "actions": ["create", "delete", "read", "update"]},
    {"resourceType": "repository", "resource": "repository", "role": "viewer", "actions": ["read"]},
    {"resourceType": "issue", "resource": "issue", "role": "owner", "actions": ["create", "delete", "read", "update"]},
    {"resourceType": "issue", "resource": "issue", "role": "collaborator", "actions": ["create", "delete", "read", "update"]},
    {"resourceType": "pull_request", "resource": "pull_request", "role": "collaborator", "actions": ["create", "delete", "read", "update"]},
    {"resourceType": "pull_request", "resource": "pull_request", "role": "viewer", "actions": ["read"]},
]


@router.get("/rebac-data")
def get_rebac_data():
    return rebac_data