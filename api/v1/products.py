from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from typing import List, Optional
from schemas.shift_assignment import ProductData
from crud.products import create_products

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
