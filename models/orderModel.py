from typing import Optional, List, Dict, Any, Annotated
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime, timezone




class Order(BaseModel):
    user_id: str  # Required ObjectId reference stored as string
    order_id: Annotated[str, Field(..., description="Provide orderId")]  # Required and unique
    product_id: str  # Required ObjectId reference stored as string
    product_details: List[str] = Field(default_factory=list)
    payment_id: str = ""
    payment_status: str = ""
    delivery_address: str = ""  # ObjectId reference stored as string
    sub_total_amt: float = 0.0  # Using float for monetary values
    total_amt: float = 0.0  # Using float for monetary values
    invoice_receipt: str = ""
    
    # Timestamp Fields
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))