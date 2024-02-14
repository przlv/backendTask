from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from db.models.shift_assignment_model import ProductDataModel
from schemas.shift_assignment import ProductData
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List, Dict


async def get_products_on_shift(key_shift: int, db: AsyncSession) -> List[Dict]:
    try:
        result = await db.execute(select(ProductDataModel).filter_by(batch_number=key_shift))
        products = result.scalars().all()
        return [jsonable_encoder(product) for product in products]
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Task not found")


async def create_products(new_products: List[ProductData], db: AsyncSession) -> None:
    async with (db.begin()):
        try:
            for product in new_products:
                new_record = ProductDataModel(**product.dict())
                existing_product = await db.execute(
                    select(ProductDataModel).filter_by(unique_product_code=product.unique_product_code)
                )
                existing_task = await db.execute(
                    select(ProductDataModel).filter_by(batch_number=new_record.batch_number)
                    .filter_by(batch_date=new_record.batch_date)
                )
                if not existing_product.first() and existing_task.first():
                    db.add(new_record)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise
