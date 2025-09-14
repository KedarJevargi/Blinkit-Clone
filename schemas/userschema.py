from pydantic import BaseModel,EmailStr,Field
from typing import Annotated

class LoginUser(BaseModel):
    email: Annotated[EmailStr,Field(...,description="user email")]
    password: Annotated[str, Field(...,min_length=6,description="user password")]



    



