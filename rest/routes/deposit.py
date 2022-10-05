from fastapi import APIRouter, HTTPException, Depends

from server import auth
from backend.buy import add_coin, reset


deposit = APIRouter(
    tags   = ['deposit'],
)


@deposit.patch('/deposit/{amount}',
    status_code = 200,
    description = 'Buyer Deposit',
    response_model = int,
)
async def deposit_add(amount: int, user: str = Depends(auth.buyer)):
    try:
        sold = add_coin(
            name = user,
            coin = amount,
        )
    except Exception as x:
        raise HTTPException(
            status_code = 400,
            detail      = f'Deposit Error ! {x}',
        )
    return sold


@deposit.patch('/reset',
    status_code = 200,
    description = 'Buyer Deposit Reset',
    response_model = int,
)
async def deposit_reset(user: str = Depends(auth.buyer)):
    try:
        sold = reset(user)
    except Exception as x:
        raise HTTPException(
            status_code = 400,
            detail      = f'Deposit Reset Error ! {x}',
        )
    return sold
