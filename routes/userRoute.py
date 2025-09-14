from fastapi import APIRouter,Request
from controllers import userController
from models import userModel
from schemas import userschema



router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/register", status_code=201)
async def register_user(request: Request, data: userModel.User):
    result = await userController.register_user_controller(request, data)
    return result
     

@router.post("/login",status_code=200)
async def login_user(request: Request, data:userschema.LoginUser):
    result = await userController.login_user_controller(request,data)
    return result

