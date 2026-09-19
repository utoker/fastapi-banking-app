from pydantic import BaseModel
from decimal import Decimal

class AccountCreate(BaseModel):
    owner_name: str

class AccountResponse(BaseModel):
    id: int
    owner_name: str
    balance: Decimal
