from fastapi import APIRouter, Depends, HTTPException
from app.services.account_service import AccountService
from app.exceptions import AccountNotFoundError
from app.dependencies import get_account_service
from app.schemas.account import AccountCreate, AccountResponse

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/", response_model=AccountResponse, status_code=201)
def open_account(account_create: AccountCreate, account_service: AccountService = Depends(get_account_service)):
    return account_service.open_account(account_create.owner_name)

@router.get("/", response_model=list[AccountResponse])
def list_accounts(account_service: AccountService = Depends(get_account_service)):
    return account_service.list_accounts()

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, account_service: AccountService = Depends(get_account_service)):
    try:
        return account_service.get_account(account_id)
    except AccountNotFoundError:
        raise HTTPException(status_code=404, detail="Account not found")