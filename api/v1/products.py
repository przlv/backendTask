from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from typing import List
from schemas.shift_assignment import ProductData
from crud.products import create_products, aggregation_product

router_products = APIRouter(
    prefix="/Products",
    tags=["Products"])


@router_products.post('/createProducts')
async def create_products_for_shift_tasks(new_products: List[ProductData],
                                          db: AsyncSession = Depends(get_db)):
    try:
        await create_products(new_products, db)
        return {'status': 'success'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router_products.post('/aggregationProduct/{id_product}')
async def aggregation_products(id_product: int,
                               unique_product_code: str,
                               db: AsyncSession = Depends(get_db)):
    try:
        return await aggregation_product(id_product, unique_product_code, db)
    except Exception as e:
        raise e
