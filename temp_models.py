from pydantic import BaseModel
from typing import Optional

class VoiceCommandRequest(BaseModel):
    command: str
    customer_name: Optional[str] = None

class SmartOrderRequest(BaseModel):
    emoji_string: str
    customer_name: Optional[str] = "Customer"

class StatusUpdate(BaseModel):
    status: str  # "paid", "pending", "failed"
