from fastapi import APIRouter, Depends,Request,Response,status
from controllers import userController
from models import userModel
from schemas import userschema
from middleware import authmiddleware



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

@router.get("/logout", status_code=status.HTTP_200_OK)
async def logout_user(
    response: Response,
    request: Request,
    user_id: str = Depends(authmiddleware.auth) # This gets the user_id
):
    # This call now correctly matches the controller's definition
    result = await userController.logout_user_controller(response, request, user_id)
    return result

