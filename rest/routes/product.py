from typing import List

from fastapi import APIRouter, HTTPException, Depends

from server import auth
from rest.model.product import ProductCre, ProductOut
from backend.products import get_product, get_products, cre_product, add_product, del_product


product = APIRouter(
    prefix = '/product',
    tags   = ['product'],
)


@product.get('/{name}',
    status_code = 200,
    description = 'Get a Product',
    response_model = ProductOut,
)
async def get_one(name: str, user: str = Depends(auth.anyone)):
    try:
        product = get_product(name)
    except Exception as x:
        raise HTTPException(
            status_code = 400,
            detail      = f'Get Product Error ! {x}',
        )
    if product:
        return product
    else:
        raise HTTPException(
            status_code = 404,
            detail      = f'Product {name} Not Found',
        )


@product.get('',
    status_code = 200,
    description = 'Get Product List',
    response_model = List[ProductOut],
)
async def get_all(user: str = Depends(auth.anyone)):
    try:
        products = get_products()
    except Exception as x:
        raise HTTPException(
            status_code = 400,
            detail      = f'Get Product Error ! {x}',
        )
    return list(products.values())


@product.post('',
    status_code = 201,
    description = 'Create a Product',
)
async def create(product: ProductCre, user: str = Depends(auth.seller)):
    try:
        cre_product(
            name   = product.name,
            seller = product.seller,
            cost   = product.cost,
        )
    except Exception as x:
        raise HTTPException(
            status_code = 400,
            detail      = f'Create Product Error ! {x}',
        )


@product.put('/{name}',
    status_code = 200,
    description = 'Add a Product',
)
async def add_one(name: str, user: str = Depends(auth.seller)):
    product = get_product(name)
    if product:
        if user != product.seller:
            raise HTTPException(
                status_code = 401,
                detail      = 'Unauthorized',
            )
    else:
        raise HTTPException(
            status_code = 404,
            detail      = f'Product {name} Not Foud',
        )

    try:
        add_product(name)
    except Exception as x:
        raise HTTPException(
            status_code = 400,
            detail      = f'Add Product Error ! {x}',
        )


@product.delete('/{name}',
    status_code = 200,
    description = 'Delete a Product',
)
async def delete_one(name: str, user: str = Depends(auth.seller)):
    product = get_product(name)
    if product:
        if user != product.seller:
            raise HTTPException(
                status_code = 401,
                detail      = 'Unauthorized',
            )
    else:
        raise HTTPException(
            status_code = 404,
            detail      = f'Product {name} Not Foud',
        )

    try:
        del_product(name)
    except Exception as x:
        raise HTTPException(
            status_code = 400,
            detail      = f'Del Product Error ! {x}',
        )
