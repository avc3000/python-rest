from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/products",
                   tags=['products'], responses={404: {"message": "Not Found"}})


class Product(BaseModel):
    id: int
    name: str


product_list = [Product(id=1, name="Mouse"), Product(id=2, name="Keyboard")]


@router.get('/')
async def get_products():
    return product_list


@router.get('/{id}')
async def get_product(id: int):
    products = filter(lambda product: product.id == id, product_list)
    return list(products)[0]
