import logging
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("ingest")

DATA_DIR = Path("data")
FILES = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}


def get_engine():
    url = (
        f"postgresql+psycopg2://{os.environ['PGUSER']}:{os.environ['PGPASSWORD']}"
        f"@{os.environ['PGHOST']}:{os.environ.get('PGPORT', '5432')}"
        f"/{os.environ['PGDATABASE']}?sslmode=require"
    )
    return create_engine(url)


def main():
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("create schema if not exists raw"))

    for table, filename in FILES.items():
        path = DATA_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing {path}. Download the dataset first.")

        df = pd.read_csv(path, dtype=str)
        df.to_sql(table, engine, schema="raw", if_exists="replace",
                  index=False, chunksize=5000, method="multi")

        with engine.connect() as conn:
            loaded = conn.execute(text(f"select count(*) from raw.{table}")).scalar()
        if loaded != len(df):
            raise RuntimeError(f"{table}: file has {len(df)} rows, database has {loaded}")
        log.info("Loaded raw.%s: %s rows", table, f"{loaded:,}")


if __name__ == "__main__":
    main()
