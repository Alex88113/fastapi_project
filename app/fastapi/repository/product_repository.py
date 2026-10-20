import asyncio
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.fastapi.shames.product import Base, ProductCreate, ProductOrm

engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/products_db")
AsyncLocalSession = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def delete_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def add_product(product: ProductCreate, db: AsyncSession):
    product_orm = ProductOrm(
        title=product.title,
        price=product.price,
        quantity=product.quantity,
        description=product.description
    )
    db.add(product_orm)
    await db.commit()
    await db.refresh(product_orm)
    return product_orm

async def get_product_by_id(id: int, db: AsyncSession):
    stmt = select(ProductOrm).where(ProductOrm.id == id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def update_product(db: AsyncSession, product_id: int, new_product: ProductCreate):
    product = await db.get(ProductOrm, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Продукта с таким ID {product_id} нет в базе.")
        
    product.title = new_product.title
    product.price = new_product.price
    product.quantity = new_product.quantity
    product.description = new_product.description
        
    await db.commit()
    await db.refresh(product)
    return product

async def delete_product(product_id: int, db: AsyncSession):
    product = await db.get(ProductOrm, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Продукта с таким ID {product_id} нет в базе.")
        
    await db.delete(product)
    await db.commit()

async def get_all_products(db: AsyncSession):
    result = await db.execute(select(ProductOrm))
    return result.scalars().all()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncLocalSession() as session:
        yield session


