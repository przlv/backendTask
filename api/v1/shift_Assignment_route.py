from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from schemas import ShiftTask, ShiftTaskChange
from typing import List, Optional
from crud.shift_assignment import (
    create_shift_task,
    get_shift_task,
    change_shift_task,
    get_filtered_shift_tasks,
)
from crud.products import get_products_on_shift
from datetime import date, datetime

router_shiftAssignment = APIRouter(prefix="/shiftAssignment", tags=["Shift Assignment"])


@router_shiftAssignment.get("/getShiftTask/{key_task}")
async def get_shift_assignment(key_task: int, db: AsyncSession = Depends(get_db)):
    try:
        required_task = await get_shift_task(key_task, db)
        required_products = await get_products_on_shift(
            required_task.get("batch_number"), db
        )
        list_products = [
            product.get("unique_product_code") for product in required_products
        ]
        return {**required_task, "products_code_on_shift": list_products}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_shiftAssignment.get("/getShiftTasks/filtered")
async def get_shift_tasks_filtered(
    closing_status: Optional[bool] = Query(None),
    batch_number: Optional[int] = Query(None),
    batch_date: Optional[date] = Query(None),
    shift_start_datetime: Optional[datetime] = Query(None),
    shift_end_datetime: Optional[datetime] = Query(None),
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    try:
        filtered_tasks = await get_filtered_shift_tasks(
            db,
            closing_status,
            batch_number,
            batch_date,
            shift_start_datetime,
            shift_end_datetime,
            offset,
            limit,
        )
        return filtered_tasks
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_shiftAssignment.post("/createShiftTask")
async def create_shift_assignment(
    shift_tasks: List[ShiftTask], db: AsyncSession = Depends(get_db)
):
    try:
        await create_shift_task(shift_tasks, db)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router_shiftAssignment.post("/change/{key_task}")
async def change_shift_assignment(
    key_task: int, new_data_task: ShiftTaskChange, db: AsyncSession = Depends(get_db)
):
    try:
        return await change_shift_task(new_data_task, key_task, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
