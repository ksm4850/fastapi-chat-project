from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_mixin, mapped_column


@declarative_mixin
class TimestampMixin:
    created_at = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
