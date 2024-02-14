from sqlalchemy import select, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from db.models.shift_assignment_model import ShiftTaskModel
from schemas.shift_assignment import ShiftTask
from typing import List, Tuple
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder


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


async def get_shift_task(key_task: int, db: AsyncSession) -> dict:
    try:
        desired_entry = await db.execute(select(ShiftTaskModel).filter_by(id=key_task))
        desired_entry = desired_entry.scalar_one()
        return jsonable_encoder(desired_entry)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Task not found")
