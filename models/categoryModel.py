from typing import Optional, List, Dict, Any, Annotated
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime, timezone



class Category(BaseModel):
    name: str = ""
    image: str = ""
    
    # Timestamp Fields
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))