from pydantic import BaseModel, Field
from decimal import Decimal

class AccountCreate(BaseModel):
    owner_name: str

class AccountResponse(BaseModel):
    id: int
    owner_name: str
    balance: Decimal

class AmountRequest(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)