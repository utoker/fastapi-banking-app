from app.models.account import Account
from decimal import Decimal

class AccountRepository:
    def __init__(self) -> None:
        self.next_id = 1
        self.accounts: dict[int, Account] = {}
    
    def create(self, owner_name: str) -> Account:
        account = Account(
            id=self.next_id,
            owner_name=owner_name,
            balance= Decimal("0")
        )
        self.accounts[self.next_id] = account
        self.next_id += 1
        return account

    def get_by_id(self, account_id: int) -> Account | None:
        return self.accounts.get(account_id)

    def list_all(self) -> list[Account]:
        return list(self.accounts.values())
