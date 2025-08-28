import os
import joblib
import pandas as pd
from dotenv import load_dotenv
import pyodbc
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from features import build_features

load_dotenv()

def read_sql_table(table):
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('SQL_SERVER')};"
        f"DATABASE={os.getenv('SQL_DB')};"
        f"UID={os.getenv('SQL_USER')};PWD={os.getenv('SQL_PWD')}"
    )
    conn = pyodbc.connect(conn_str, autocommit=True)
    return pd.read_sql(f"SELECT * FROM {table}", conn)

def read_csv_local():
    # fallback for local demo - loads CSVs if DB not available
    sales = pd.read_csv("../data/sample_sales.csv", parse_dates=["date_key"])
    calendar = pd.DataFrame({
        "date_key": pd.to_datetime(sales["date_key"].unique()),
    })
    calendar["dow"] = calendar["date_key"].dt.weekday + 1
    calendar["is_holiday"] = 0
    products = pd.DataFrame([
        {"product_id":101, "category":"Beverages", "price":2.99},
        {"product_id":102, "category":"Snacks", "price":1.49},
    ])
    stores = pd.DataFrame([
        {"store_id":1, "city":"Aurangabad", "region":"MH"},
        {"store_id":2, "city":"Pune", "region":"MH"},
    ])
    return sales, calendar, products, stores

def main():
    try:
        sales = read_sql_table("dbo.Sales")
        calendar = read_sql_table("dbo.Calendar")
        products = read_sql_table("dbo.Products")
        stores = read_sql_table("dbo.Stores")
    except Exception as e:
        print("Could not connect to SQL Server, falling back to local CSV sample:", e)
        sales, calendar, products, stores = read_csv_local()

    # ensure date_key is datetime
    sales["date_key"] = pd.to_datetime(sales["date_key"])
    calendar["date_key"] = pd.to_datetime(calendar["date_key"])

    X, y = build_features(sales, calendar, products, stores)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = mean_squared_error(y_test, preds, squared=False)
    print(f"Validation RMSE: {rmse:.3f}")

    os.makedirs("models", exist_ok=True)
    bundle = {"model": model, "feature_cols": list(X.columns)}
    joblib.dump(bundle, "models/model.joblib")
    print("Saved models/model.joblib")

if __name__ == "__main__":
    main()

