from app.repositories.account_repository import AccountRepository
from app.services.account_service import AccountService

repo = AccountRepository()

def get_account_service() -> AccountService:
    return AccountService(repo)