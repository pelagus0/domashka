from __future__ import annotations

from datetime import date

import psycopg


DSN = "postgresql://postgres:postgres@localhost:5438/cian"


def exec_file(conn: psycopg.Connection, path: str) -> None:
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
        cur.execute("TRUNCATE op_log, copy, edition, work RESTART IDENTITY CASCADE;")
        cur.executemany(
            "INSERT INTO work (id, title) VALUES (%s, %s);",
            [(1, "A"), (2, "B"), (3, "C")],
        )
        # Work 1 has 6 editions
        for idx in range(1, 7):
            cur.execute(
                "INSERT INTO edition (work_id, year, pages) VALUES (%s, %s, %s);",
                (1, 2000 + idx, 100 + idx),
            )
        cur.execute(
            "INSERT INTO edition (work_id, year, pages) VALUES (%s, %s, %s);",
            (2, 2020, 200),
        )
        cur.execute(
            "INSERT INTO edition (work_id, year, pages) VALUES (%s, %s, %s);",
            (3, 2021, 150),
        )
        # Copies
        cur.execute(
            "INSERT INTO copy (edition_id, inventory_number) VALUES (%s, %s);",
            (1, "INV-1"),
        )
        cur.execute(
            "INSERT INTO copy (edition_id, inventory_number) VALUES (%s, %s);",
            (2, "INV-2"),
        )
        cur.execute(
            "INSERT INTO copy (edition_id, inventory_number) VALUES (%s, %s);",
            (7, "INV-3"),
        )
        cur.execute(
            "INSERT INTO copy (edition_id, inventory_number) VALUES (NULL, %s);",
            ("INV-NO-ED",),
        )
        # Logs
        cur.executemany(
            "INSERT INTO op_log (user_id, copy_id, taken_at, returned_at) VALUES (%s, %s, %s, %s);",
            [
                (1, 1, date(2025, 1, 1), date(2025, 1, 10)),
                (1, 2, date(2025, 2, 1), None),
                (1, 3, date(2025, 2, 10), date(2025, 4, 20)),
                (2, 1, date(2025, 3, 1), date(2025, 3, 2)),
                (2, 2, date(2025, 3, 5), date(2025, 3, 6)),
                (2, 3, date(2025, 3, 10), date(2025, 3, 11)),
                (2, 1, date(2025, 3, 12), date(2025, 3, 13)),
                (2, 2, date(2025, 3, 14), date(2025, 3, 15)),
            ],
        )
    conn.commit()


def main() -> None:
    with psycopg.connect(DSN) as conn:
        exec_file(conn, "queries.sql")
        seed(conn)
        exec_file(conn, "queries.sql")


if __name__ == "__main__":
    main()

