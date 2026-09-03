import duckdb
import os
import logging

logger = logging.getLogger(__name__)

def load_silver():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bronze_path = os.path.join(base_dir, 'data', 'lake', '01_bronze', 'online_retail.parquet')
    silver_path = os.path.join(base_dir, 'data', 'lake', '02_silver')

    os.makedirs(silver_path, exist_ok=True)
    con = duckdb.connect()

    # Facts
    logger.info(f"[lake] Creating fact_sales at: {os.path.join(silver_path, 'fact_sales.parquet')}...")

    con.execute(f"""
        COPY (
            SELECT  InvoiceNo                               AS invoice_no,
                    StockCode                               AS stock_code,
                    CAST(Quantity AS INTEGER)               AS quantity,
                    STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M') AS invoice_date,
                    CustomerID                              AS customer_id
            FROM    read_parquet('{bronze_path}')
            WHERE   Quantity > 0
                AND CustomerID IS NOT NULL 
        ) TO '{os.path.join(silver_path, 'fact_sales.parquet')}' (FORMAT PARQUET)
    """)

    # Dims
    logger.info(f"[lake] Creating dim_customer at: {os.path.join(silver_path, 'dim_customer.parquet')}...")

    con.execute(f"""
        COPY (
            SELECT  DISTINCT CustomerID AS customer_id,
                    Country             AS country
            FROM    read_parquet('{bronze_path}')
        ) TO '{os.path.join(silver_path, 'dim_customer.parquet')}' (FORMAT PARQUET)
    """)

    logger.info(f"[lake] Creating dim_product at: {os.path.join(silver_path, 'dim_product.parquet')}...")

    con.execute(f"""
        COPY (
            SELECT  DISTINCT StockCode        AS stock_code,
                    Description               AS description,
                    CAST(UnitPrice AS DOUBLE) AS unit_price
            FROM    read_parquet('{bronze_path}')
        ) TO '{os.path.join(silver_path, 'dim_product.parquet')}' (FORMAT PARQUET)
    """)

    con.close()

    logger.info(f"[lake] Silver Layer created at: {silver_path}")

if __name__ == "__main__":
    load_silver()