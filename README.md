# Retail Demand Forecasting Tool

Advanced analytics tool built to predict weekly product demand across stores using Azure SQL, Python ML, and a small C# API gateway.

## Features
- Train baseline Random Forest model (scikit-learn) and optional TensorFlow DNN.
- FastAPI-based inference service (Python).
- C# (.NET 8) minimal API gateway that proxies inference.
- Dockerized services and sample GitHub Actions CI/CD for pushing container images and deploying to Azure Web Apps.
- SQL Server / Azure SQL schema + seed data.

## Quickstart (local)
1. Clone the repo.
2. Create a `.env` from `.env.example` and fill values.
3. Populate the database: run `sql/01_schema.sql` then `sql/02_seed.sql` on your SQL Server/Azure SQL.
4. Train model:
   ```bash
   cd ml
   pip install -r requirements.txt
   python train_sklearn.py
