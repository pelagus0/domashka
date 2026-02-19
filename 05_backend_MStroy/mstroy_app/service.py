from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from mstroy_app.models import Item
from mstroy_app.treestore import TreeStore


def load_items_as_dicts(db_session: Session) -> list[dict]:
    items = list(db_session.execute(select(Item)).scalars().all())
    result: list[dict] = []
    for item in items:
        payload = dict(item.payload)
        parent: int | str | None
        if item.parent_id is None:
            parent = "root"
        else:
            parent = item.parent_id
        payload.update({"id": item.id, "parent": parent})
        result.append(payload)
    return result


def seed_items(db_session: Session) -> int:
    sample = [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None},
    ]

    db_session.execute(delete(Item))
    db_session.commit()

    for item in sample:
        parent = item["parent"]
        parent_id = None if parent == "root" else int(parent)
        payload = {key: value for key, value in item.items() if key not in {"id", "parent"}}
        db_session.add(Item(id=int(item["id"]), parent_id=parent_id, payload=payload))
    db_session.commit()
    return len(sample)


def build_tree_store(db_session: Session) -> TreeStore:
    return TreeStore(load_items_as_dicts(db_session))

