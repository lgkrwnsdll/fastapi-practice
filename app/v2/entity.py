from datetime import datetime
from typing import Optional, List

from sqlalchemy import (
    BigInteger, String, DateTime, ForeignKey
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship
)


class BaseEntity(DeclarativeBase, AsyncAttrs):
    pass


class Parent(BaseEntity):
    __tablename__ = "parent"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    children: Mapped[List["Child"]] = relationship(
        "Child",
        back_populates="parent",
        cascade="all, delete-orphan"
    )


class Child(BaseEntity):
    __tablename__ = "child"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    parent_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("parent.id"),
        nullable=True,
        index=True
    )

    parent: Mapped[Optional[Parent]] = relationship(
        "Parent",
        back_populates="children"
    )
