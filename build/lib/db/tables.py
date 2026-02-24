from typing import Optional
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    place: Mapped[Optional[str]] = mapped_column(String)
    query: Mapped[Optional[str]] = mapped_column(String)
    count: Mapped[Optional[int]] = mapped_column(Integer)
    is_subscribed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    timezone: Mapped[Optional[str]] = mapped_column(String)
