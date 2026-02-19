-- Schema
CREATE TABLE IF NOT EXISTS users (
  user_id integer PRIMARY KEY,
  age integer NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
  item_id integer PRIMARY KEY,
  price numeric NOT NULL
);

CREATE TABLE IF NOT EXISTS purchases (
  purchase_id integer PRIMARY KEY,
  user_id integer NOT NULL REFERENCES users(user_id),
  item_id integer NOT NULL REFERENCES items(item_id),
  purchased_at date NOT NULL
);

-- A) Average monthly spend by age groups
-- 18-25
WITH per_user_month AS (
  SELECT
    p.user_id,
    date_trunc('month', p.purchased_at)::date AS month,
    SUM(i.price) AS spend
  FROM purchases p
  JOIN items i ON i.item_id = p.item_id
  JOIN users u ON u.user_id = p.user_id
  WHERE u.age BETWEEN 18 AND 25
  GROUP BY p.user_id, date_trunc('month', p.purchased_at)::date
)
SELECT AVG(spend) AS avg_monthly_spend_18_25
FROM per_user_month;

-- 26-35
WITH per_user_month AS (
  SELECT
    p.user_id,
    date_trunc('month', p.purchased_at)::date AS month,
    SUM(i.price) AS spend
  FROM purchases p
  JOIN items i ON i.item_id = p.item_id
  JOIN users u ON u.user_id = p.user_id
  WHERE u.age BETWEEN 26 AND 35
  GROUP BY p.user_id, date_trunc('month', p.purchased_at)::date
)
SELECT AVG(spend) AS avg_monthly_spend_26_35
FROM per_user_month;

-- B) Month with max revenue from users 35+
SELECT
  date_trunc('month', p.purchased_at)::date AS month,
  SUM(i.price) AS revenue
FROM purchases p
JOIN items i ON i.item_id = p.item_id
JOIN users u ON u.user_id = p.user_id
WHERE u.age >= 35
GROUP BY date_trunc('month', p.purchased_at)::date
ORDER BY revenue DESC
LIMIT 1;

-- C) Item with max revenue in the last 12 months (relative to max purchase date)
WITH bounds AS (
  SELECT MAX(purchased_at) AS max_date FROM purchases
),
period AS (
  SELECT (max_date - interval '12 months')::date AS from_date, max_date AS to_date
  FROM bounds
)
SELECT
  p.item_id,
  SUM(i.price) AS revenue
FROM purchases p
JOIN items i ON i.item_id = p.item_id
JOIN period t ON p.purchased_at > t.from_date AND p.purchased_at <= t.to_date
GROUP BY p.item_id
ORDER BY revenue DESC
LIMIT 1;

-- D) Top-3 items by revenue and their share for a given year (example: 2025)
WITH year_purchases AS (
  SELECT
    p.item_id,
    SUM(i.price) AS revenue
  FROM purchases p
  JOIN items i ON i.item_id = p.item_id
  WHERE EXTRACT(YEAR FROM p.purchased_at) = 2025
  GROUP BY p.item_id
),
total AS (
  SELECT SUM(revenue) AS total_revenue FROM year_purchases
)
SELECT
  yp.item_id,
  yp.revenue,
  (yp.revenue / NULLIF(t.total_revenue, 0))::numeric(10, 4) AS share
FROM year_purchases yp
CROSS JOIN total t
ORDER BY yp.revenue DESC
LIMIT 3;

