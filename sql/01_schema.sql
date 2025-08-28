IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'dbo') BEGIN END;
GO

CREATE TABLE IF NOT EXISTS dbo.Calendar (
  date_key DATE PRIMARY KEY,
  dow TINYINT,
  is_holiday BIT
);

CREATE TABLE IF NOT EXISTS dbo.Products (
  product_id INT PRIMARY KEY,
  category NVARCHAR(50),
  price DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS dbo.Stores (
  store_id INT PRIMARY KEY,
  city NVARCHAR(50),
  region NVARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dbo.Sales (
  date_key DATE NOT NULL,
  product_id INT NOT NULL,
  store_id INT NOT NULL,
  units_sold INT NOT NULL,
  PRIMARY KEY (date_key, product_id, store_id),
  FOREIGN KEY (date_key) REFERENCES dbo.Calendar(date_key),
  FOREIGN KEY (product_id) REFERENCES dbo.Products(product_id),
  FOREIGN KEY (store_id) REFERENCES dbo.Stores(store_id)
);
GO

