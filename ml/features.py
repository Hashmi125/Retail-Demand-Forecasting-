import pandas as pd

def build_features(df_sales, df_calendar, df_products, df_stores):
    """
    Input:
      - df_sales: columns [date_key, product_id, store_id, units_sold]
      - df_calendar: columns [date_key, dow, is_holiday]
      - df_products: columns [product_id, category, price]
      - df_stores: columns [store_id, city, region]

    Returns:
      - X (DataFrame features), y (Series target)
    """
    df = df_sales.merge(df_calendar, on="date_key", how="left") \
                 .merge(df_products, on="product_id", how="left") \
                 .merge(df_stores, on="store_id", how="left")

    df = df.sort_values(["product_id", "store_id", "date_key"]).reset_index(drop=True)

    # Lag features
    df["lag_1"] = df.groupby(["product_id", "store_id"])["units_sold"].shift(1)
    df["lag_7"] = df.groupby(["product_id", "store_id"])["units_sold"].shift(7)

    # Rolling mean - 7 days
    df["roll7"] = df.groupby(["product_id", "store_id"])["units_sold"] \
                    .rolling(window=7, min_periods=1).mean().reset_index(0, drop=True)

    # Cast and fill
    df["dow"] = df["dow"].astype(int)
    df["is_holiday"] = df["is_holiday"].fillna(0).astype(int)
    df["price"] = df["price"].fillna(df["price"].mean()).astype(float)

    # Drop rows with missing lag_1 or lag_7 to keep features consistent
    df = df.dropna(subset=["lag_1", "lag_7"])

    feature_cols = ["dow", "is_holiday", "price", "lag_1", "lag_7", "roll7", "store_id", "product_id"]
    target_col = "units_sold"
    X = df[feature_cols].copy()
    y = df[target_col].copy()
    return X, y

