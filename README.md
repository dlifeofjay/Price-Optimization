# Price Optimization

This repository contains a price optimization project built with Python, Streamlit, and FastAPI. The solution demonstrates how to use a trained demand prediction model to evaluate pricing decisions, compare profit and demand outcomes, and surface the results in an interactive dashboard.

## Project Overview

The project is designed to help people selling typical goods or services estimate how demand and profit change when prices are adjusted. It combines a demand prediction model with a price-scenario analysis engine and exposes the results through a Streamlit-based interface.

The main capabilities are:
- interactive selection of product and promotion inputs
- demand prediction for a given price
- generation of a price range to evaluate demand and profit outcomes
- visualization of price vs demand and price vs profit
- model evaluation dashboard for actual vs predicted demand on test data

## Architecture

- `app.py`: Streamlit entry point for the dashboard application.
- `frontend/dashboard.py`: Interactive UI for running price optimization and comparing profit vs demand scenarios.
- `frontend/evaluation.py`: UI for model evaluation using test data and feature importance.
- `backend/main.py`: FastAPI application for exposing a price optimization endpoint.
- `backend/modelling.py`: Core modeling logic that loads the preprocessor and trained model, generates price scenarios, predicts demand, and computes profit.

## Data and Artifacts

- `backend/Data/test_data.npy`: Test dataset with actual and predicted demand values used by the evaluation dashboard.
- `backend/Artifacts/preprocessor.pkl`: Saved preprocessing pipeline used to transform inputs before prediction.
- `backend/Artifacts/optim_model.pkl`: Trained demand prediction model.
- `backend/Data/Feature_Imp.parquet`: Feature importance information for model explainability.
- `backend/Data/fulfilment_center_info.csv` and `backend/Data/meal_info.csv`: Supporting data files related to branches and meal items.

## Usage

### Run the Streamlit dashboard

1. Activate the Python virtual environment.
2. Install dependencies if needed:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. Use the sidebar to select week, branch, meal, price, promotion options, discount, and increase percentage.
5. Click `Run Optimization` to generate the price optimization analysis.

### Run the FastAPI backend

1. Activate the Python virtual environment.
2. Install dependencies if needed.
3. Start the API server:
   ```bash
   uvicorn backend.main:app --reload
   ```
4. The API exposes a health check endpoint at `/health` and a price optimization endpoint at `/price_optim`.

## API Contract

The `/price_optim` endpoint accepts a JSON payload with the following fields:

- `week`: integer
- `branch`: integer
- `meal`: integer
- `current_price`: float
- `email_promo`: boolean
- `app_homepage_promo`: boolean
- `discount_percent`: integer
- `product_category`: string
- `product_cuisine`: string
- `percent_increase`: integer

And returns:
- `price_range`: list of tested prices
- `demand_list`: list of predicted demand values
- `profit_list`: list of profit values
- `predicted_demand`: baseline predicted demand at the current price

## Model Behavior

The price optimization logic in `backend/modelling.py`:
- predicts demand using the loaded model for the selected input features
- generates a price range from 90% of the current price up to the current price plus the selected increase percentage
- predicts demand for each price in that range
- computes profit assuming cost is 70% of price

This provides a simple decision-support tool for comparing profit-driven pricing and demand-driven pricing.

## Requirements

The project depends on:

- Python
- Streamlit
- FastAPI
- Plotly
- pandas
- numpy
- scikit-learn
- joblib
- requests
- pyarrow

The exact versions are listed in `requirements.txt`.

## Notes

- The project is structured as a portfolio demonstration and is focused on the pricing optimization workflow rather than production-grade deployment.
- The modelling logic relies on local artifact files in `backend/Artifacts` and assumes those files are present.
- The evaluation page is useful for validating that the demand model is reasonably aligned with unseen test data.
