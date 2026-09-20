from app.exceptions import AccountNotFoundError, InsufficientFundsError, TransferError
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

    def withdraw(self, account_id: int, amount: Decimal) -> Account:
        account = self.get_account(account_id)
        
        if amount > account.balance:
            raise InsufficientFundsError(f"Account with ID {account_id} has insufficient funds")
        new_balance = account.balance - amount
        account.balance = new_balance
        return self.account_repository.update(account)

    def transfer(self, from_account_id: int, to_account_id: int, amount: Decimal) -> tuple[Account, Account]:
        if from_account_id == to_account_id:
            raise TransferError("Cannot transfer to the same account")

        to_account = self.get_account(to_account_id)
        from_account = self.withdraw(from_account_id, amount)
        to_account = self.deposit(to_account_id, amount)

        return (from_account, to_account)
