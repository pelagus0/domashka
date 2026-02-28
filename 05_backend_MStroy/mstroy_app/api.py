from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mstroy_app.db import get_db
from mstroy_app.schemas import ItemOut, SeedResult
from mstroy_app.service import build_tree_store, seed_items

router = APIRouter(prefix="/api/v1")


@router.post("/items/seed", response_model=SeedResult)
def seed(db_session: Session = Depends(get_db)) -> SeedResult:
    inserted = seed_items(db_session)
    return SeedResult(inserted=inserted)


@router.get("/items", response_model=list[dict])
def get_all(db_session: Session = Depends(get_db)) -> list[dict]:
    store = build_tree_store(db_session)
    return store.getAll()


@router.get("/items/{item_id}", response_model=dict)
def get_item(item_id: int, db_session: Session = Depends(get_db)) -> dict:
    store = build_tree_store(db_session)
    item = store.getItem(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/items/{item_id}/children", response_model=list[dict])
def get_children(item_id: int, db_session: Session = Depends(get_db)) -> list[dict]:
    store = build_tree_store(db_session)
    return store.getChildren(item_id)


@router.get("/items/{item_id}/parents", response_model=list[dict])
def get_parents(item_id: int, db_session: Session = Depends(get_db)) -> list[dict]:
    store = build_tree_store(db_session)
    return store.getAllParents(item_id)

