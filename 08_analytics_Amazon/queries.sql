-- Task 1: clients who bought iPhone but not Airpods
CREATE TABLE IF NOT EXISTS orders (
  order_id serial PRIMARY KEY,
  client_id integer NOT NULL,
  item text NOT NULL,
  ordered_at date NOT NULL
);

SELECT DISTINCT o.client_id
FROM orders o
WHERE o.item = 'iPhone'
  AND NOT EXISTS (
    SELECT 1
    FROM orders o2
    WHERE o2.client_id = o.client_id AND o2.item = 'Airpods'
  )
ORDER BY o.client_id;

-- Task 2 (simplified): subscription history normalization
CREATE TABLE IF NOT EXISTS subscriptions (
  sub_id serial PRIMARY KEY,
  user_id integer NOT NULL,
  started_at date NOT NULL,
  ended_at date NOT NULL,
  status text NOT NULL
);

-- Example: monthly active subscription days per user
WITH days AS (
  SELECT
    user_id,
    generate_series(started_at, ended_at, interval '1 day')::date AS d
  FROM subscriptions
  WHERE status = 'active'
)
SELECT
  user_id,
  date_trunc('month', d)::date AS month,
  COUNT(*) AS active_days
FROM days
GROUP BY user_id, date_trunc('month', d)::date
ORDER BY user_id, month;

