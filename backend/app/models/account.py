from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Account:
    id: int
    owner_name: str
    balance: Decimal