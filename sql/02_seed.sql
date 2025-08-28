-- Insert products and stores
INSERT INTO dbo.Products (product_id, category, price) VALUES (101, 'Beverages', 2.99);
INSERT INTO dbo.Products (product_id, category, price) VALUES (102, 'Snacks', 1.49);

INSERT INTO dbo.Stores (store_id, city, region) VALUES (1, 'Aurangabad', 'MH');
INSERT INTO dbo.Stores (store_id, city, region) VALUES (2, 'Pune', 'MH');

-- Minimal calendar for January 2025
WITH d AS (
  SELECT CAST('2025-01-01' AS DATE) AS d
  UNION ALL
  SELECT DATEADD(DAY, 1, d) FROM d WHERE d < '2025-01-31'
)
INSERT INTO dbo.Calendar(date_key, dow, is_holiday)
SELECT d, DATEPART(WEEKDAY, d), CASE WHEN d IN ('2025-01-01') THEN 1 ELSE 0 END
FROM d OPTION (MAXRECURSION 0);

-- Synthetic sales sample
INSERT INTO dbo.Sales (date_key, product_id, store_id, units_sold)
SELECT TOP (200) d.date_key, p.product_id, s.store_id,
       ABS(CHECKSUM(NEWID())) % 50 + CASE WHEN DATEPART(WEEKDAY,d.date_key) IN (1,7) THEN 10 ELSE 0 END
FROM dbo.Calendar d
CROSS JOIN dbo.Products p
CROSS JOIN dbo.Stores s
ORDER BY d.date_key;

