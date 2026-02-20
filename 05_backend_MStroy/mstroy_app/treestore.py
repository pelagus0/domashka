from __future__ import annotations

from collections import defaultdict


class TreeStore:
    def __init__(self, items: list[dict]) -> None:
        self._items = items
        self._by_id = {item["id"]: item for item in items}
        by_parent: dict[object, list[dict]] = defaultdict(list)
        for item in items:
            by_parent[item.get("parent")].append(item)
        self._by_parent = dict(by_parent)

    def getAll(self) -> list[dict]:
        return self._items

    def getItem(self, item_id: int) -> dict | None:
        return self._by_id.get(item_id)

    def getChildren(self, item_id: int) -> list[dict]:
        return self._by_parent.get(item_id, [])

    def getAllParents(self, item_id: int) -> list[dict]:
        item = self.getItem(item_id)
        if item is None:
            return []
        parents: list[dict] = []
        current = item
        while current.get("parent") != "root":
            parent_id = current.get("parent")
            if parent_id is None:
                break
            parent_item = self.getItem(int(parent_id))
            if parent_item is None:
                break
            parents.append(parent_item)
            current = parent_item
        return parents

