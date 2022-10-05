from fastapi import APIRouter, HTTPException, Depends

from server import auth
from rest.model.buy import BuyReq, BuyResp
from backend.buy import buy_products


buy = APIRouter(
    prefix = '/buy',
    tags   = ['buy'],
)


@buy.post('',
    status_code = 200,
    description = 'Buy Products',
    response_model = BuyResp,
)
async def buying(req: BuyReq, user: str = Depends(auth.buyer)):
    try:
        return buy_products(req, user)
    except Exception as x:
        raise HTTPException(
            status_code = 400,
            detail      = f'Buy Error ! {x}',
        )
