MerchTech – GMV Diagnostic Prototype (Brief Notes)

Tech: Django REST Framework + React (Vite + Tailwind)
Goal: Diagnose why certain products underperform in GMV.

1. Context:-
Merch Tech needs a system to identify issues causing GMV drop. The prototype must ingest reviews, returns, and sales data, analyze it, and surface top issues + recommended actions.

2. Problem Solved:-
The system automatically processes 4 provided datasets:
sde2_merchtech_dataset.json
sde2_reviews.csv
sde2_returns.csv
sde2_sales.csv

It generates actionable insights per product, including:
-> GMV performance summary
-> Top issues (rating drop, high return rate, negative sentiment, low sales weeks)
-> Suggested corrective actions
-> Weekly sales summary
-> Review keyword extraction
-> Aggregated return reasons

3. How It Works (Prototype Flow):-
Django Backend:-
-> Loads datasets (CSV + JSON) into in-memory structures.
-> Runs analysis modules: sentiment processing, return clustering, weekly sales summary, GMV calculation.
-> Combines outputs into unified product-level insights.

Provides endpoints:
-> GET /api/analyze/ – full insights
-> GET /api/analyze/<asin>/ – single product

Automation
Custom Django command:
python manage.py generate_insights
→ outputs insights_auto.json

React Frontend
Dedicated dashboard showing: total products, reviews, returns.
Product cards → Product Details page with issues, actions, return reasons, weekly sales table.
Clean UI using Tailwind + reusable components.

4. Installation
Backend (Django):
cd backend
python -m venv .venv
venv\Scripts\activate (For virtual env activate)
pip install -r requirements.txt
python manage.py runserver

Frontend (React):
cd frontend
npm install
npm run dev

Place all dataset files inside:
backend/analysis/data

5. How GMV Is Calculated
GMV = sum of weekly sales revenue, based on the sales CSV.
If gmv column represents per-row revenue → GMV = Σ(row.gmv).
If it represents per-unit revenue → GMV = units_sold × gmv.

6. Deliverables Provided:-
-> Working Django API + React frontend
-> Automated insights generator (generate_insights)
-> Dataset ingestion + analysis modules
-> Full repo structure + code
