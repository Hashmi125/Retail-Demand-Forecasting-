# Retail Demand Forecasting Tool

Advanced analytics tool using Azure and SQL to build predictive demand models.

## Tech Stack
- SQL Server / Azure SQL
- Python (Scikit-learn, TensorFlow, FastAPI)
- C# (.NET 8 minimal API)
- Docker + GitHub Actions

Retail-Demand-Forecasting/

├─ data/sample_sales.csv

├─ sql/01_schema.sql

├─ sql/02_seed.sql

├─ ml/requirements.txt

├─ ml/features.py

├─ ml/train_sklearn.py

├─ ml/inference_service.py

├─ api-gateway-csharp/Program.cs

├─ api-gateway-csharp/RetailForecast.Api.csproj

├─ Dockerfile.python

├─ Dockerfile.csharp

├─ .github/workflows/python-api-azure.yml

├─ .github/workflows/csharp-api-azure.yml

├─ README.md

└─ .gitignore
└─ .env.example
