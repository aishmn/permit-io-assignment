from fastapi import APIRouter, Depends
from services.permit_service import PermitService

router = APIRouter()
permit_service = PermitService()

@router.get("/")
def read_roles():
    return permit_service.get_roles()
