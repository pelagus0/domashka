from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import psycopg


@dataclass(frozen=True, slots=True)
class DbConfig:
    dsn: str = "postgresql://postgres:postgres@localhost:5439/amazon"


def reverse_list_inplace(values: list[int]) -> list[int]:
    left = 0
    right = len(values) - 1
    while left < right:
        values[left], values[right] = values[right], values[left]
        left += 1
        right -= 1
    return values


def reverse_list_slice(values: list[int]) -> list[int]:
    return values[::-1]


def reverse_list_reversed(values: list[int]) -> list[int]:
    return list(reversed(values))


def exec_sql(conn: psycopg.Connection, path: str) -> None:
    with open(path, "r", encoding="utf-8") as handle:
        content = handle.read()
    statements = [chunk.strip() for chunk in content.split(";") if chunk.strip()]
    with conn.cursor() as cur:
        for statement in statements:
            cur.execute(statement)
            if cur.description:
                rows = cur.fetchall()
                print(statement.splitlines()[0], "->", rows)
    conn.commit()


def seed(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute("TRUNCATE subscriptions, orders RESTART IDENTITY CASCADE;")
        cur.executemany(
            "INSERT INTO orders (client_id, item, ordered_at) VALUES (%s, %s, %s);",
            [
                (1, "iPhone", date(2025, 1, 1)),
                (1, "Case", date(2025, 1, 2)),
                (2, "iPhone", date(2025, 1, 3)),
                (2, "Airpods", date(2025, 1, 4)),
                (3, "Airpods", date(2025, 1, 5)),
                (4, "iPhone", date(2025, 1, 6)),
            ],
        )
        cur.executemany(
            "INSERT INTO subscriptions (user_id, started_at, ended_at, status) VALUES (%s, %s, %s, %s);",
            [
                (10, date(2025, 1, 1), date(2025, 1, 10), "active"),
                (10, date(2025, 2, 1), date(2025, 2, 5), "active"),
                (11, date(2025, 1, 15), date(2025, 2, 15), "active"),
                (12, date(2025, 1, 1), date(2025, 1, 3), "cancelled"),
            ],
        )
    conn.commit()


def main() -> None:
    values = [1, 2, 3, 4, 5]
    print("reverse inplace:", reverse_list_inplace(values.copy()))
    print("reverse slice:", reverse_list_slice(values.copy()))
    print("reverse reversed:", reverse_list_reversed(values.copy()))

    config = DbConfig()
    with psycopg.connect(config.dsn) as conn:
        exec_sql(conn, "queries.sql")
        seed(conn)
        exec_sql(conn, "queries.sql")


if __name__ == "__main__":
    main()

