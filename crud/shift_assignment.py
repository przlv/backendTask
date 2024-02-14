from datetime import date, datetime
from typing import Dict, List, Optional, Sequence

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.shift_assignment_model import ShiftTaskModel
from schemas.shift_assignment import ShiftTask, ShiftTaskChange


async def create_shift_task(json_tasks: List[ShiftTask], db: AsyncSession) -> None:
    async with db.begin():
        try:
            for task in json_tasks:
                new_record = ShiftTaskModel(**task.dict())
                db.add(new_record)
            await db.commit()
        except Exception:
            await db.rollback()
            raise


async def get_shift_task(key_task: int, db: AsyncSession) -> Dict:
    try:
        required_entry = await db.execute(select(ShiftTaskModel).filter_by(id=key_task))
        required_entry = required_entry.scalar_one()
        return jsonable_encoder(required_entry)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Task not found")


async def change_shift_task(
    new_data_task: ShiftTaskChange, key_task: int, db: AsyncSession
) -> Dict:
    async with db.begin():
        try:
            required_entry = await db.execute(
                select(ShiftTaskModel).filter_by(id=key_task)
            )
            entry = required_entry.scalar_one()

            for key, value in new_data_task.dict().items():
                if value is not None:
                    if key == "closing_status":
                        entry.closed_at = datetime.now() if value else None
                        setattr(entry, key, value)
                    else:
                        setattr(entry, key, value)

            await db.commit()
            return entry
        except NoResultFound:
            await db.rollback()
            raise HTTPException(status_code=404, detail="Task not found")


async def get_filtered_shift_tasks(
    db: AsyncSession,
    closing_status: Optional[bool] = None,
    batch_number: Optional[int] = None,
    batch_date: Optional[date] = None,
    shift_start_datetime: Optional[datetime] = None,
    shift_end_datetime: Optional[datetime] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Sequence[ShiftTaskModel]:

    query = select(ShiftTaskModel)

    if closing_status is not None:
        query = query.filter(ShiftTaskModel.closing_status == closing_status)
    if batch_number is not None:
        query = query.filter(ShiftTaskModel.batch_number == batch_number)
    if batch_date is not None:
        query = query.filter(ShiftTaskModel.batch_date == batch_date)
    if shift_start_datetime is not None:
        query = query.filter(
            ShiftTaskModel.shift_start_datetime >= shift_start_datetime
        )
    if shift_end_datetime is not None:
        query = query.filter(ShiftTaskModel.shift_end_datetime <= shift_end_datetime)

    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)

    try:
        result = await db.execute(query)
        tasks = result.scalars().all()
        if not tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
