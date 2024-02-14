from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    UniqueConstraint,
    Date,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductDataModel(Base):
    __tablename__ = "product_data"

    id = Column(Integer, primary_key=True)
    unique_product_code = Column(String, unique=True)
    batch_number = Column(Integer)
    batch_date = Column(Date)
    is_aggregated = Column(Boolean, default=False)
    aggregated_at = Column(DateTime, nullable=True)


class ShiftTaskModel(Base):
    __tablename__ = "shift_tasks"

    id = Column(Integer, primary_key=True)
    closing_status = Column(Boolean)
    closed_at = Column(DateTime)
    shift_task_representation = Column(String)
    work_center = Column(String)
    shift = Column(String)
    brigade = Column(String)
    batch_number = Column(Integer)
    batch_date = Column(Date)
    nomenclature = Column(String)
    ekn_code = Column(String)
    rc_identifier = Column(String)
    shift_start_datetime = Column(DateTime(timezone=True))
    shift_end_datetime = Column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("batch_number", "batch_date", name="unique_batch_number_date"),
    )
