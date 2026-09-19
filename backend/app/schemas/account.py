from pydantic import BaseModel

class AccountCreate(BaseModel):
    owner_name: str

class AccountResponse(BaseModel):
    id: int
    owner_name: str
    balance: Decimal
