from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from mstroy_app.db import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("items.id", ondelete="SET NULL"),
        nullable=True,
    )
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)

