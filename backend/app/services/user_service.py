from permit import Permit

async def sync_user(permit: Permit, user_email: str):
    user = await permit.api.users.sync({
        "key": user_email,
        "email": user_email,
    })
    return user

async def assign_role(permit: Permit, user_email: str, role: str):
    await permit.api.users.assign_role({
        "user": user_email,
        "role": role,
        "tenant": "default",
    })
