import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from db.models.shift_assignment_model import ProductDataModel
from schemas.shift_assignment import ProductData
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List, Dict


async def get_products_on_shift(key_shift: int,
                                db: AsyncSession) -> List[Dict]:
    try:
        result = await db.execute(select(ProductDataModel)
                                  .filter_by(batch_number=key_shift))
        products = result.scalars().all()
        return [jsonable_encoder(product) for product in products]
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Task not found")


async def create_products(new_products: List[ProductData],
                          db: AsyncSession) -> None:
    async with (db.begin()):
        try:
            for product in new_products:
                new_record = ProductDataModel(**product.dict())
                existing_product = await db.execute(
                    select(ProductDataModel)
                    .filter_by(unique_product_code=product.unique_product_code)
                )
                existing_task = await db.execute(
                    select(ProductDataModel)
                    .filter_by(batch_number=new_record.batch_number)
                    .filter_by(batch_date=new_record.batch_date)
                )
                if not existing_product.first() and existing_task.first():
                    db.add(new_record)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e


async def aggregation_product(id_product: int,
                              unique_product_code: str,
                              db: AsyncSession) -> Dict:
    async with (db.begin()):
        try:
            product = await db.execute(
                select(ProductDataModel)
                .filter_by(unique_product_code=unique_product_code)
            )
            product = product.scalars().first()
            if product:
                if product.is_aggregated:
                    raise HTTPException(status_code=400,
                                        detail=f'unique code already used at '
                                               f'{product.aggregated_at}')
                elif product.id != id_product:
                    raise HTTPException(status_code=400,
                                        detail='unique code is attached '
                                               'to another batch')
                else:
                    setattr(product, 'is_aggregated', True)
                    setattr(product, 'aggregated_at', datetime.datetime.now())
                    await db.commit()
                    return jsonable_encoder(product)
            else:
                raise HTTPException(status_code=404,
                                    detail='Product not found')
        except Exception as e:
            await db.rollback()
            raise e
