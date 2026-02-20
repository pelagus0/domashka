from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import psycopg


@dataclass(frozen=True, slots=True)
class DbConfig:
    dsn: str = "postgresql://postgres:postgres@localhost:5437/wib"


def _seed_data(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute("TRUNCATE purchases, items, users RESTART IDENTITY CASCADE;")

        cur.executemany(
            "INSERT INTO users (user_id, age) VALUES (%s, %s);",
            [
                (1, 20),
                (2, 24),
                (3, 27),
                (4, 33),
                (5, 40),
                (6, 52),
            ],
        )
        cur.executemany(
            "INSERT INTO items (item_id, price) VALUES (%s, %s);",
            [
                (10, 100),
                (11, 250),
                (12, 500),
                (13, 25),
            ],
        )
        cur.executemany(
            "INSERT INTO purchases (purchase_id, user_id, item_id, purchased_at) VALUES (%s, %s, %s, %s);",
            [
                (1000, 1, 10, date(2025, 1, 10)),
                (1001, 1, 11, date(2025, 1, 12)),
                (1002, 2, 13, date(2025, 2, 3)),
                (1003, 3, 12, date(2025, 2, 11)),
                (1004, 4, 11, date(2025, 3, 8)),
                (1005, 5, 12, date(2025, 3, 9)),
                (1006, 5, 12, date(2025, 12, 30)),
                (1007, 6, 10, date(2025, 12, 29)),
            ],
        )


def _exec_sql_file(conn: psycopg.Connection, path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as handle:
        content = handle.read()
    statements = [chunk.strip() for chunk in content.split(";") if chunk.strip()]
    results: list[str] = []
    with conn.cursor() as cur:
        for statement in statements:
            cur.execute(statement)
            if cur.description:
                rows = cur.fetchall()
                results.append(f"{statement.splitlines()[0][:60]}... -> {rows}")
            else:
                results.append(f"{statement.splitlines()[0][:60]}... -> OK")
    conn.commit()
    return results


def main() -> None:
    config = DbConfig()
    with psycopg.connect(config.dsn) as conn:
        outputs = _exec_sql_file(conn, "queries.sql")
        _seed_data(conn)
        outputs = _exec_sql_file(conn, "queries.sql")

    for line in outputs:
        print(line)


if __name__ == "__main__":
    main()

