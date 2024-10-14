import os
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from permit import Permit


permit = Permit(
    pdp=os.getenv('PERMIT_PDP_URL', 'https://cloudpdp.api.permit.io'),
    token=os.getenv("PERMIT_API_KEY")
)

user = {
    "id": "owner3@gmail.com",
    "firstName": "mr",
    "lastName": "owner",
    "email": "owner3@gmail.com",
}

origins = ["http://localhost:3000"]

async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def check_permissions():
    permitted = await permit.check(user["id"], "read", "repository")
    testdata = await permit.api._resources.list()
    print(testdata)
    if not permitted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "result": f"{user.get('firstName')} {user.get('lastName')} is NOT PERMITTED to read document!"
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "result": f"{user.get('firstName')} {user.get('lastName')} is PERMITTED to read document!"
        }
    )

def convert_to_serializable(data):
    if isinstance(data, list):
        return [convert_to_serializable(item) for item in data]
    elif hasattr(data, '__dict__'):
        return {key: convert_to_serializable(value) for key, value in data.__dict__.items()}
    elif isinstance(data, dict):
        return {key: convert_to_serializable(value) for key, value in data.items()}
    else:
        return str(data)

@app.get("/rbac-data/roles")
async def get_rbac_data():
    try:
        rbac_data = await permit.api._roles.list()
        rbac_data_serializable = convert_to_serializable(rbac_data)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"rbac_data": rbac_data_serializable})

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@app.get("/rbac-data/resources")
async def get_rbac_data():
    try:
        rbac_data = await permit.api._resources.list()

        rbac_data_serializable = convert_to_serializable(rbac_data)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"rbac_data": rbac_data_serializable})

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))