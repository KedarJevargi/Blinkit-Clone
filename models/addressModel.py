from typing import Optional, List, Dict, Any, Annotated
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone






class Address(BaseModel):
    address_line: str = ""
    city: str = ""
    state: str = ""
    pincode: Optional[str] = None  # Required field in mongoose, no default
    country: Optional[str] = None  # Required field in mongoose, no default
    mobile: Optional[int] = None
    status: bool = True
    user_id: str = ""  # ObjectId reference stored as string
    
    # Timestamp Fields
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
