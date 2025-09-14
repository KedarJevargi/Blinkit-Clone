from pydantic import BaseModel,EmailStr,Field
from typing import Annotated

class RegisterUser(BaseModel):
    name: Annotated[str,Field(...,description="user first and last name")] 
    email: Annotated[EmailStr,Field(...,description="user email")]
    password: Annotated[str, Field(...,min_length=6,description="user password")]
    



