from fastapi import HTTPException, Depends, Request
from permit import Permit
import os
import jwt

permit = Permit(
    pdp="http://permit-pdp:7000",
    token=os.getenv("PERMIT_API_KEY")
)

SECRET_KEY = os.getenv("JWT_SECRET")
def get_user_key(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]  
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def Enforcer(resource_key: str, action_name: str, context: dict = None):
    if context is None:
        context = {}

    async def permit_dependency(user_key: str = Depends(get_user_key)):
        allowed = await permit.check(
            user=user_key,
            action=action_name,
            resource=resource_key,
            context=context
        )

        if not allowed:
            raise HTTPException(status_code=403, detail="Access denied")

    return permit_dependency