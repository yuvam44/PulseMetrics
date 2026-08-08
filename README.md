# 📊 PulseMetrics — AI-Powered Business Analytics Platform

PulseMetrics is a Streamlit-based analytics dashboard combining three tools:
market analysis, demand forecasting (Linear Regression), and a business KPI
dashboard — built to demonstrate practical data analysis and machine learning
skills using Python.

## Features

- **Market Analysis** — Upload product/market CSVs and get automatic pricing,
  rating, and competition metrics, with interactive charts and a computed
  Opportunity Score.
- **Demand Forecasting** — Trains a Linear Regression model on historical
  monthly sales to forecast 1, 3, 6, or 12 months ahead, with an R²-based
  confidence explanation.
- **Business KPI Dashboard** — 20+ KPIs (revenue, growth, conversion,
  inventory, customer satisfaction, a composite Business Health Score) with
  filterable date ranges and CSV export.

## Tech Stack

Python, Streamlit, Pandas, NumPy, Scikit-learn, Plotly, OpenPyXL

## Running Locally

git clone https://github.com/yourusername/PulseMetrics.git
cd PulseMetrics
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

## Project Structure

PulseMetrics/
├── app.py
├── tools/
│   ├── market_analysis.py
│   ├── forecasting.py
│   └── kpi_dashboard.py
├── data/
├── requirements.txt
└── README.md

## Notes

Opportunity Score, Competition Score, and Business Health Score are
custom rule-based composite metrics designed for this project, not
outputs of a trained ML model. The forecasting tool uses a genuine
trained Linear Regression model via scikit-learn.