from pydantic import BaseModel,EmailStr,Field
from typing import Annotated,Optional

class LoginUser(BaseModel):
    email: Annotated[EmailStr,Field(...,description="user email")]
    password: Annotated[str, Field(...,min_length=6,description="user password")]



    


class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = Field(
        default=None, min_length=10, max_length=10, pattern=r'^[0-9]+$'
    )
    password: Optional[str] = Field(default=None, min_length=6)


class ForgotPassword(BaseModel):
    email: Annotated[EmailStr,Field(...,description="user email")]








