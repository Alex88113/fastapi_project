from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi import Depends


from app.fastapi.shames.product import ProductCreate, ProductOrm
from app.fastapi.repository.product_repository import (
    add_product,
    update_product,
    delete_product,
    get_all_products
)
from app.fastapi.repository.product_repository import get_db

router = APIRouter(tags=['products'])

@router.post("/products")
async def create_product(product: ProductCreate, db: AsyncSession=Depends(get_db)) -> dict[str, str]:
    if product.price < 0:
        raise HTTPException(status_code=422, detail="Цена на продукт не может быть отрицательной")

    await add_product(product, db)
    return {"message": f"Продукт успешно создан и внесен в Базу данных, его ID {product.id}"}


@router.get('/products')
async def get_all_products_endpoints(db: AsyncSession=Depends(get_db)):
    return await get_all_products(db)

@router.get('/products/{product_id}')
async def get_product(product_id: int, db: AsyncSession=Depends(get_db)):
    return await db.get(ProductOrm, product_id)


@router.put('/products/{product_id}')
async def update_product_endpoint(product_id: int, new_product: ProductCreate, db: AsyncSession=Depends(get_db)):
    return await update_product(db, product_id, new_product)


@router.delete("/products/{product_id}")
async def delete_product_from_db(product_id: int, db: AsyncSession=Depends(get_db)):
    await delete_product(product_id, db)
    return {"message": f"Продукт по ID {product_id} удалён."}
