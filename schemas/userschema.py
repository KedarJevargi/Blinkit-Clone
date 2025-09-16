from pydantic import BaseModel,EmailStr,Field, model_validator
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

class VerifyForgotPasswordOtp(BaseModel):
    email: EmailStr
    otp: str = Field(..., description="The 6-digit OTP sent to the user's email")


class ResetPassword(BaseModel):
    email: EmailStr
    new_password: str = Field(..., min_length=6, description="The user's new password")
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'ResetPassword':
        if self.new_password != self.confirm_password:
            raise ValueError('New password and confirmation password do not match.')
        return self




