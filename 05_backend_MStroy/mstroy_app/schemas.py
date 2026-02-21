from __future__ import annotations

from pydantic import BaseModel


class ItemOut(BaseModel):
    id: int
    parent: int | str | None
    payload: dict


class SeedResult(BaseModel):
    inserted: int

