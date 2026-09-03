import pandas as pd
import os
from deltalake.writer import write_deltalake
import logging

logger = logging.getLogger(__name__)

def load_bronze():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, 'data', 'raw', 'OnlineRetail.csv')
    bronze_path = os.path.join(base_dir, 'data', 'lakehouse', '01_bronze', 'online_retail')

    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"[lakehouse] Raw file not found at: {raw_path}")

    logger.info(f"[lakehouse] Reading raw file at: {raw_path}")

    df = pd.read_csv(raw_path, encoding='ISO-8859-1', dtype={'CustomerID': str})

    write_deltalake(bronze_path, df, mode='overwrite')

    logger.info(f"[lakehouse] Bronze layer created at: {bronze_path}")

if __name__ == "__main__":
    load_bronze()