from typing import Optional, List, Dict, Any, Annotated
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime, timezone




class Product(BaseModel):
    name: Optional[str] = None  # Required field in mongoose but no default
    image: List[str] = Field(default_factory=list)  # Array in mongoose
    category: List[str] = Field(default_factory=list)  # ObjectId references stored as strings
    sub_category: List[str] = Field(default_factory=list)  # ObjectId references stored as strings
    unit: str = ""
    stock: Optional[int] = None
    price: Optional[float] = None  # Note: there was a typo "defualt" in mongoose schema
    discount: Optional[float] = None
    description: str = ""
    more_details: Dict[str, Any] = Field(default_factory=dict)  # Object type in mongoose
    publish: bool = True
    
    # Timestamp Fields
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))