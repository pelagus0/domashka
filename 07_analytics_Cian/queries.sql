-- Schema (3NF)
CREATE TABLE IF NOT EXISTS work (
  id serial PRIMARY KEY,
  title text NOT NULL
);

CREATE TABLE IF NOT EXISTS edition (
  id serial PRIMARY KEY,
  work_id integer NOT NULL REFERENCES work(id),
  year integer NOT NULL,
  pages integer NOT NULL
);

CREATE TABLE IF NOT EXISTS copy (
  id serial PRIMARY KEY,
  edition_id integer REFERENCES edition(id),
  inventory_number text NOT NULL
);

CREATE TABLE IF NOT EXISTS op_log (
  id serial PRIMARY KEY,
  user_id integer NOT NULL,
  copy_id integer NOT NULL REFERENCES copy(id),
  taken_at date NOT NULL,
  returned_at date
);

-- 1) Works published more than 5 times
SELECT w.id, w.title, COUNT(e.id) AS editions_count
FROM work w
JOIN edition e ON e.work_id = w.id
GROUP BY w.id, w.title
HAVING COUNT(e.id) > 5;

-- 2) Copies not linked to any edition
SELECT c.id, c.inventory_number
FROM copy c
WHERE c.edition_id IS NULL;

-- 3) For each user: last 3 taken works + total times taken overall
WITH taken AS (
  SELECT
    l.user_id,
    w.id AS work_id,
    w.title,
    l.taken_at,
    ROW_NUMBER() OVER (PARTITION BY l.user_id ORDER BY l.taken_at DESC) AS rn
  FROM op_log l
  JOIN copy c ON c.id = l.copy_id
  JOIN edition e ON e.id = c.edition_id
  JOIN work w ON w.id = e.work_id
),
counts AS (
  SELECT
    w.id AS work_id,
    COUNT(*) AS total_taken
  FROM op_log l
  JOIN copy c ON c.id = l.copy_id
  JOIN edition e ON e.id = c.edition_id
  JOIN work w ON w.id = e.work_id
  GROUP BY w.id
)
SELECT t.user_id, t.work_id, t.title, t.taken_at, c.total_taken
FROM taken t
JOIN counts c ON c.work_id = t.work_id
WHERE t.rn <= 3
ORDER BY t.user_id, t.taken_at DESC;

-- 4) Unreliable users: example score by 2+ criteria
-- Criteria:
-- - overdue returns (returned_at > taken_at + 30 days OR not returned)
-- - high borrow count
WITH stats AS (
  SELECT
    user_id,
    COUNT(*) AS borrows,
    SUM(
      CASE
        WHEN returned_at IS NULL THEN 1
        WHEN returned_at > taken_at + interval '30 days' THEN 1
        ELSE 0
      END
    ) AS overdue
  FROM op_log
  GROUP BY user_id
)
SELECT
  user_id,
  borrows,
  overdue,
  (borrows + overdue * 5) AS score
FROM stats
WHERE overdue > 0 OR borrows >= 5
ORDER BY score DESC
LIMIT 10;

