
from typing import Optional, List, Annotated
from pydantic import BaseModel, EmailStr, Field 
from enum import Enum  
from datetime import datetime, timezone





class Status(str, Enum):
    active = "Active"
    inactive = "Inactive"
    suspended = "Suspended"


class Role(str, Enum):
    admin = "ADMIN"
    user = "USER"


class User(BaseModel):

    name: Annotated[str,Field(...,description="user full name")] 
    email: Annotated[EmailStr,Field(...,description="user email")]  
    password: Annotated[str,Field(...,min_length=6)] 

    # --- Optional Fields & Fields with Defaults ---
    # These fields are not required at creation. They either have a default value or can be `None`.
    avatar: str = ""  # Defaults to an empty string if not provided.
    mobile: Optional[str] = None  # The value can be a string or `None`.
    refresh_token: str = ""
    verify_email: bool = False  # Defaults to `False`.
    last_login_date: Optional[datetime] = None  # Can be a `datetime` object or `None`.
    status: Status = Status.active  # Defaults to the `active` member of the `Status` enum.
    role: Role = Role.user  # Defaults to the `user` member of the `Role` enum.
    forgot_password_otp: Optional[str] = None
    forgot_password_expiry: Optional[datetime] = None

    # --- List Fields ---
    # These fields are lists that will likely store string representations of ObjectIds from other collections.
    # `Field(default_factory=list)` is used to create a new empty list for each new instance of the User model.
    # This prevents different User objects from accidentally sharing the same list in memory.
    address_details: List[str] = Field(default_factory=list)
    shopping_cart: List[str] = Field(default_factory=list)
    order_history: List[str] = Field(default_factory=list)

    # --- Timestamp Fields ---
    # These correspond to the `timestamps: true` option in Mongoose, which automatically adds `createdAt` and `updatedAt`.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

 