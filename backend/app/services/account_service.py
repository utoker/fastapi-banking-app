from app.exceptions import AccountNotFoundError
from app.models.account import Account
from decimal import Decimal
from app.repositories.account_repository import AccountRepository

class AccountService:
    def __init__(self, account_repository: AccountRepository) -> None:
        self.account_repository = account_repository

    def open_account(self, owner_name: str) -> Account:
        return self.account_repository.create(owner_name)

    def get_account(self, account_id: int) -> Account:
        account = self.account_repository.get_by_id(account_id)
        if account is None:
            raise AccountNotFoundError(f"Account with ID {account_id} not found")
        return account

    def list_accounts(self) -> list[Account]:
        return self.account_repository.list_all()

    def deposit(self, account_id: int, amount: Decimal) -> Account:
        account = self.get_account(account_id)
        new_balance = account.balance + amount
        account.balance = new_balance
        return self.account_repository.update(account)