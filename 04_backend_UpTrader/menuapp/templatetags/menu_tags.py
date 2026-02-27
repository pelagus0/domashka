from __future__ import annotations

from dataclasses import dataclass

from django import template
from django.db.models import Prefetch
from django.urls import NoReverseMatch, reverse

from menuapp.models import Menu, MenuItem

register = template.Library()


@dataclass(frozen=True, slots=True)
class Node:
    item: MenuItem
    children: list["Node"]
    expanded: bool
    active: bool


def _resolve_item_url(item: MenuItem) -> str:
    if item.url:
        return item.url
    if item.named_url:
        try:
            return reverse(item.named_url)
        except NoReverseMatch:
            return "#"
    return "#"


def _build_tree(items: list[MenuItem]) -> dict[int | None, list[MenuItem]]:
    by_parent: dict[int | None, list[MenuItem]] = {}
    for item in items:
        parent_id = item.parent_id
        by_parent.setdefault(parent_id, []).append(item)
    return by_parent


def _find_active(items: list[MenuItem], current_path: str) -> MenuItem | None:
    for item in items:
        if _resolve_item_url(item) == current_path:
            return item
    return None


def _collect_ancestors(active: MenuItem, items_by_id: dict[int, MenuItem]) -> set[int]:
    expanded_ids: set[int] = set()
    current = active
    while current.parent_id is not None:
        expanded_ids.add(current.parent_id)
        current = items_by_id[current.parent_id]
    return expanded_ids


def _make_nodes(
    parent_id: int | None,
    by_parent: dict[int | None, list[MenuItem]],
    expanded_ids: set[int],
    active_id: int | None,
) -> list[Node]:
    nodes: list[Node] = []
    for item in by_parent.get(parent_id, []):
        is_active = item.id == active_id
        is_expanded = item.id in expanded_ids or is_active
        children = _make_nodes(item.id, by_parent, expanded_ids, active_id) if is_expanded else []
        nodes.append(Node(item=item, children=children, expanded=is_expanded, active=is_active))
    return nodes


@register.inclusion_tag("menuapp/menu.html", takes_context=True)
def draw_menu(context: dict, menu_name: str) -> dict:
    request = context["request"]
    current_path = request.path

    # Exactly 1 query for the whole menu: join menu + items
    menu = (
        Menu.objects.filter(name=menu_name)
        .prefetch_related(
            Prefetch("items", queryset=MenuItem.objects.select_related("parent")),
        )
        .first()
    )
    if menu is None:
        return {"nodes": [], "current_path": current_path}

    items = list(menu.items.all())
    items_by_id = {item.id: item for item in items}

    active = _find_active(items, current_path)
    expanded_ids: set[int] = set()
    active_id: int | None = None
    if active is not None:
        active_id = active.id
        expanded_ids = _collect_ancestors(active, items_by_id)
        # also expand first level below active:
        expanded_ids.add(active_id)

    by_parent = _build_tree(items)
    nodes = _make_nodes(None, by_parent, expanded_ids, active_id)

    return {"nodes": nodes, "current_path": current_path}

