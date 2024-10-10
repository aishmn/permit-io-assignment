from fastapi import APIRouter, Depends
from services.permit_service import PermitService

router = APIRouter()
permit_service = PermitService()

@router.get("/resources")
def read_resources():
    return permit_service.get_resources()
