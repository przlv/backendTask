from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ProductDataModel(Base):
    __tablename__ = 'product_data'

    id = Column(Integer, primary_key=True)
    unique_product_code = Column(String, unique=True)
    batch_number = Column(Integer, unique=True)
    batch_date = Column(DateTime)
    is_aggregated = Column(Boolean, default=False)
    aggregated_at = Column(DateTime, nullable=True)

    shift_tasks = relationship("ShiftTaskModel", back_populates="product_data")


class ShiftTaskModel(Base):
    __tablename__ = 'shift_tasks'

    id = Column(Integer, primary_key=True)
    closing_status = Column(Boolean)
    closed_at = Column(DateTime)
    shift_task_representation = Column(String)
    work_center = Column(String)
    shift = Column(String)
    brigade = Column(String)
    batch_number = Column(Integer, ForeignKey('product_data.batch_number'))
    batch_date = Column(DateTime)
    nomenclature = Column(String)
    ekn_code = Column(String)
    rc_identifier = Column(String)
    shift_start_datetime = Column(DateTime)
    shift_end_datetime = Column(DateTime)

    product_data = relationship("ProductDataModel", back_populates="shift_tasks")
    __table_args__ = (UniqueConstraint('batch_number', 'batch_date', name='unique_batch_number_date'),)
