from fastapi import APIRouter, Depends
from services.permit_service import PermitService

router = APIRouter()
permit_service = PermitService()

@router.get("/users")
def read_users():
    return permit_service.get_users()
