from typing import Optional, List, Dict, Any, Annotated
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime, timezone



class CartProduct(BaseModel):
    product_id: str  # Required ObjectId reference stored as string
    quantity: int = 1
    user_id: str  # Required ObjectId reference stored as string
    
    # Timestamp Fields
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))