from fastapi import APIRouter



router = APIRouter(
    prefix="/user",
    tags=["User"]
)

# @router.post("/register", status_code=201)
# async def register_user():
#     pass

