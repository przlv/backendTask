from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class ShiftTask(BaseModel):
    closing_status: bool = Field(..., validation_alias='СтатусЗакрытия')
    closed_at: Optional[datetime] = None
    shift_task_representation: str = Field(..., validation_alias='ПредставлениеЗаданияНаСмену')
    work_center: str = Field(..., validation_alias='РабочийЦентр')
    shift: str = Field(..., validation_alias='Смена')
    brigade: str = Field(..., validation_alias='Бригада')
    batch_number: int = Field(..., validation_alias='НомерПартии')
    batch_date: date = Field(..., validation_alias='ДатаПартии')
    nomenclature: str = Field(..., validation_alias='Номенклатура')
    ekn_code: str = Field(..., validation_alias='КодЕКН')
    rc_identifier: str = Field(..., validation_alias='ИдентификаторРЦ')
    shift_start_datetime: datetime = Field(..., validation_alias='ДатаВремяНачалаСмены')
    shift_end_datetime: datetime = Field(..., validation_alias='ДатаВремяОкончанияСмены')

    class Config:
        allow_population_by_field_name = True


class ProductData(BaseModel):
    unique_product_code: str = Field(..., alias='УникальныйКодПродукта')
    batch_number: int = Field(..., alias='НомерПартии')
    batch_date: datetime = Field(..., alias='ДатаПартии')
    is_aggregated: Optional[bool] = None
    aggregated_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
