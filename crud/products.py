from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from db.models.shift_assignment_model import ProductDataModel
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
