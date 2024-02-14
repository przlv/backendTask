from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from schemas import ShiftTask
from typing import List
from crud.shift_assignment import create_shift_task, get_shift_task
from crud.products import get_products_on_shift

router_shiftAssignment = APIRouter(
    prefix="/shiftAssignment",
    tags=["Shift Assignment"])


@router_shiftAssignment.post('/createShiftTask')
async def create_shift_assignment(shift_tasks: List[ShiftTask], db: AsyncSession = Depends(get_db)):
    try:
        await create_shift_task(shift_tasks, db)
        return {'status': 'success'}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router_shiftAssignment.get('/getShiftTask/{key_task}')
async def get_shift_assignment(key_task: int, db: AsyncSession = Depends(get_db)):
    try:
        desired_task = await get_shift_task(key_task, db)
        desired_products = await get_products_on_shift(desired_task.get('batch_number'), db)
        list_products = [product.get('unique_product_code') for product in desired_products]
        return {
            **desired_task,
            'products_code_on_shift': list_products
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
