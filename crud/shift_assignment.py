from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from db.models.shift_assignment_model import ShiftTaskModel
from schemas.shift_assignment import ShiftTask, ShiftTaskChange
from typing import List, Dict
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from datetime import datetime


async def create_shift_task(json_tasks: List[ShiftTask], db: AsyncSession) -> None:

    async with db.begin():
        try:
            for task in json_tasks:
                new_record = ShiftTaskModel(**task.dict())
                db.add(new_record)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise


async def get_shift_task(key_task: int, db: AsyncSession) -> Dict:
    try:
        required_entry = await db.execute(select(ShiftTaskModel).filter_by(id=key_task))
        required_entry = required_entry.scalar_one()
        return jsonable_encoder(required_entry)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Task not found")


async def change_shift_task(new_data_task: ShiftTaskChange, key_task: int, db: AsyncSession) -> Dict:
    async with db.begin():
        try:
            required_entry = await db.execute(select(ShiftTaskModel).filter_by(id=key_task))
            entry = required_entry.scalar_one()

            for key, value in new_data_task.dict().items():
                if value is not None:
                    if key == 'closing_status':
                        entry.closed_at = datetime.now() if value else None
                        setattr(entry, key, value)
                    else:
                        setattr(entry, key, value)

            await db.commit()
            return entry
        except NoResultFound:
            await db.rollback()
            raise HTTPException(status_code=404, detail="Task not found")
