from datetime import datetime

from sqlalchemy import String, func, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    title: str = Field(min_length=3)
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)
    description: str | None = None

class Base(DeclarativeBase):
    pass

class ProductOrm(Base):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float]
    quantity: Mapped[int]
    description: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
