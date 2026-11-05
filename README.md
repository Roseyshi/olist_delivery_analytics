# Olist Delivery Performance Analytics

An end-to-end analytics engineering project that answers one business question:

> **Where and why are deliveries late, and how much does lateness hurt customer reviews?**

The project ingests raw e-commerce data into PostgreSQL, cleans and models it with dbt, tests data quality, answers business questions in SQL, and presents the findings in a dashboard.

**Status:** work in progress. See the [roadmap](#roadmap) for what is finished and what is next.

<!-- Add a dashboard screenshot when ready: docs/dashboard.png -->
<!-- ![Dashboard](docs/dashboard.png) -->

## Dataset

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle): roughly 100,000 anonymised orders from 2016 to 2018, spread across related tables (orders, items, payments, customers, sellers, products and reviews).

The raw CSV files are not included in this repository. Download them from Kaggle, check the dataset's licence terms on that page, and credit Olist if you reuse the data.

## Business metrics

Defined once and reused everywhere:

| Metric | Definition |
|---|---|
| Late order | Delivered to the customer after the estimated delivery date |
| Delivery days | Purchase date to customer delivery date |
| Days late | Delivery date minus estimated date, when positive |
| On-time rate | Share of delivered orders that were not late |

## Architecture

```
Olist CSVs -> Python ingest (raw schema) -> PostgreSQL
           -> dbt: staging models -> marts (fct_deliveries)
           -> SQL business questions -> dashboard
           -> GitHub Actions: load, dbt build, tests
```

1. **Ingest.** `ingest/load_raw.py` loads each CSV into a `raw` schema exactly as received (as text) and checks that the row count in the database matches the file.
2. **Transform.** dbt staging models clean and type the data. Cleaning logic lives in versioned SQL, not in notebooks.
3. **Test.** dbt tests check uniqueness, non-null keys, accepted values and relationships, plus a custom test for impossible dates.
4. **Analyse.** SQL queries answer the business questions (CTEs, joins and window functions).
5. **Present.** A dashboard summarises the headline finding and the supporting breakdowns.

## Tech stack

- **PostgreSQL** (hosted on Neon or Supabase free tier)
- **Python** (pandas, SQLAlchemy) for ingestion
- **dbt Core** for transformations and tests
- **SQL** for analysis
- **pytest** for validation logic
- **GitHub Actions** for automation
- **Power BI / Tableau** for the dashboard

## Repository structure

```
.
├── ingest/                 # load_raw.py (and validation helpers)
├── dbt_project/
│   ├── models/staging/     # stg_orders, stg_reviews, sources and tests
│   ├── models/marts/       # fct_deliveries (planned)
│   └── tests/              # custom data tests
├── sql/                    # commented business-question queries (planned)
├── tests/                  # pytest tests (planned)
├── dashboard/              # screenshots and exports (planned)
├── docs/                   # data quality notes, case study
├── .env.example            # connection settings template
├── requirements.txt
└── README.md
```

## Getting started

```bash
git clone https://github.com/Roseyshi/olist-delivery-analytics.git
cd olist-delivery-analytics
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

1. Download the Olist CSVs from Kaggle into `data/`.
2. Copy `.env.example` to `.env` and fill in your PostgreSQL connection details. Never commit `.env`.
3. Load the raw data:
   ```bash
   python ingest/load_raw.py
   ```
4. Load the environment variables into your terminal, then run dbt from the `dbt_project` folder:
   ```bash
   cd dbt_project
   dbt debug --profiles-dir .
   dbt run --profiles-dir .
   dbt test --profiles-dir .
   ```

## Data quality

Data issues found during testing, and how each was handled, are recorded in [`docs/data_quality_notes.md`](docs/data_quality_notes.md). Examples include orders with more than one review (the latest review is kept so the model has one review per order) and any records where delivery dates precede purchase dates.

## Findings

*To be completed once the analysis is finished.* This section will summarise:

- Late-delivery rate overall and by state
- Sellers and regions that contribute most to lateness
- The relationship between days late and review score
- A recommendation based on the results, and its limitations

## Roadmap

- [x] Raw ingestion into PostgreSQL with row-count checks
- [x] dbt staging models for orders and reviews, with tests
- [ ] Remaining staging models (items, sellers, customers)
- [ ] `fct_deliveries` mart (one row per delivered order)
- [ ] 8 to 10 SQL business questions
- [ ] Dashboard and headline finding
- [ ] GitHub Actions workflow for load and tests
- [ ] pytest tests for validation rules
- [ ] Case study write-up

## Limitations

- The data covers 2016 to 2018 and is a single marketplace, so results describe that period and are not a forecast.
- The dataset is static, so any scheduled run reloads the same data rather than new orders.
- Correlation between lateness and review scores does not prove that lateness alone causes low ratings.

## Acknowledgements

Data: Olist, via Kaggle. Please follow the licence terms on the dataset page.

## Author

Roseline Wahome, [LinkedIn](https://www.linkedin.com/in/roseline-wahome-dataanalyst/) | [GitHub](https://github.com/Roseyshi) | [Portfolio](https://roseyshi.github.io/Portfolio)
