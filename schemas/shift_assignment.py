from pydantic import BaseModel, Field, Extra
from typing import Optional
from datetime import date, datetime


class ShiftTask(BaseModel):
    closing_status: bool = Field(..., validation_alias='СтатусЗакрытия')
    shift_task_representation: str = Field(...,
                                           validation_alias='Представление'
                                                            'ЗаданияНаСмену')
    work_center: str = Field(..., validation_alias='Линия')
    shift: str = Field(..., validation_alias='Смена')
    brigade: str = Field(..., validation_alias='Бригада')
    batch_number: int = Field(..., validation_alias='НомерПартии')
    batch_date: date = Field(..., validation_alias='ДатаПартии')
    nomenclature: str = Field(..., validation_alias='Номенклатура')
    ekn_code: str = Field(..., validation_alias='КодЕКН')
    rc_identifier: str = Field(..., validation_alias='ИдентификаторРЦ')
    shift_start_datetime: datetime = Field(...,
                                           validation_alias='ДатаВремя'
                                                            'НачалаСмены')
    shift_end_datetime: datetime = Field(...,
                                         validation_alias='ДатаВремя'
                                                          'ОкончанияСмены')

    class Config:
        allow_population_by_field_name = True
        extra = Extra.forbid


class ProductData(BaseModel):
    unique_product_code: str = Field(..., alias='УникальныйКодПродукта')
    batch_number: int = Field(..., alias='НомерПартии')
    batch_date: date = Field(..., alias='ДатаПартии')
    is_aggregated: Optional[bool] = None
    aggregated_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        extra = Extra.forbid


class ShiftTaskChange(BaseModel):
    closing_status: Optional[bool] = Field(None)
    shift_task_representation: Optional[str] = Field(None)
    work_center: Optional[str] = Field(None)
    shift: Optional[str] = Field(None)
    brigade: Optional[str] = Field(None)
    batch_number: Optional[int] = Field(None)
    batch_date: Optional[date] = Field(None)
    nomenclature: Optional[str] = Field(None)
    ekn_code: Optional[str] = Field(None)
    rc_identifier: Optional[str] = Field(None)
    shift_start_datetime: Optional[datetime] = Field(None)
    shift_end_datetime: Optional[datetime] = Field(None)

    class Config:
        extra = Extra.forbid
