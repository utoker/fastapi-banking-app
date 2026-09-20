from fastapi import APIRouter, Depends, HTTPException
from app.services.account_service import AccountService
from app.exceptions import AccountNotFoundError, InsufficientFundsError, TransferError
from app.dependencies import get_account_service
from app.schemas.account import AccountCreate, AccountResponse, AmountRequest, TransferRequest, TransferResponse

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
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{account_id}/deposit", response_model=AccountResponse)
def deposit(account_id: int, amount_request: AmountRequest, account_service: AccountService = Depends(get_account_service)):
    try:
        return account_service.deposit(account_id, amount_request.amount)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{account_id}/withdraw", response_model=AccountResponse)
def withdraw(account_id: int, amount_request: AmountRequest, account_service: AccountService = Depends(get_account_service)):
    try:
        return account_service.withdraw(account_id, amount_request.amount)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InsufficientFundsError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.post("/{account_id}/transfer", response_model=TransferResponse)
def transfer(account_id: int, transfer_request: TransferRequest, account_service: AccountService = Depends(get_account_service)):
    try:
        from_account, to_account = account_service.transfer(account_id, transfer_request.to_account_id, transfer_request.amount)
        return TransferResponse(
            from_account_id=account_id,
            to_account_id=transfer_request.to_account_id,
            amount=transfer_request.amount,
            from_account_balance=from_account.balance,
            to_account_balance=to_account.balance
        )
    except TransferError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InsufficientFundsError as e:
        raise HTTPException(status_code=409, detail=str(e))