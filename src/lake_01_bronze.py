import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

def load_bronze():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, 'data', 'raw', 'OnlineRetail.csv')
    bronze_path = os.path.join(base_dir, 'data', 'lake', '01_bronze')

    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"[lake] Raw file not found at: {raw_path}")

    logger.info(f"[lake] Reading raw file at: {raw_path}")

    df = pd.read_csv(raw_path, encoding='ISO-8859-1', dtype={'CustomerID': str})

    os.makedirs(bronze_path, exist_ok=True)

    df.to_parquet(os.path.join(bronze_path, 'online_retail.parquet'), index=False)

    logger.info(f"[lake] Bronze layer created at: {bronze_path}")

if __name__ == "__main__":
    load_bronze()