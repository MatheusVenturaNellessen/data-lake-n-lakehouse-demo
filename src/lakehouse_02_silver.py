import duckdb
import os
from deltalake import DeltaTable
from deltalake.writer import write_deltalake
import logging

logger = logging.getLogger(__name__)

def load_silver():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bronze_path = os.path.join(base_dir, 'data', 'lakehouse', '01_bronze', 'online_retail')
    silver_path = os.path.join(base_dir, 'data', 'lakehouse', '02_silver')

    con = duckdb.connect()

    dt = DeltaTable(bronze_path)
    con.register('bronze', dt.to_pyarrow_dataset())

    # Fact
    logger.info(f"[lakehouse] Creating fact_sales at: {os.path.join(silver_path, 'fact_sales')}...")

    df_fact_sales = con.execute(f"""
        SELECT  InvoiceNo                               AS invoice_no,
                StockCode                               AS stock_code,
                CAST(Quantity AS INTEGER)               AS quantity,
                STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M') AS invoice_date,
                CustomerID                              AS customer_id
        FROM    bronze
        WHERE   Quantity > 0
            AND CustomerID IS NOT NULL 
    """).df()
    write_deltalake(os.path.join(silver_path, 'fact_sales'), df_fact_sales, mode="overwrite")

    # Dims
    logger.info(f"[lakehouse] Creating dim_customer at:{os.path.join(silver_path, 'dim_customer')}...")

    df_dim_product = con.execute(f"""
        SELECT  DISTINCT CustomerID AS customer_id,
                Country             AS country
        FROM    bronze
    """).df()
    write_deltalake(os.path.join(silver_path, 'dim_customer'), df_dim_product, mode="overwrite")

    logger.info(f"[lakehouse] Creating dim_product at: {os.path.join(silver_path, 'dim_product')}...")

    df_dim_customer = con.execute(f"""
        SELECT  DISTINCT StockCode        AS stock_code,
                Description               AS description,
                CAST(UnitPrice AS DOUBLE) AS unit_price
        FROM    bronze
    """).df()
    write_deltalake(os.path.join(silver_path, 'dim_product'), df_dim_customer, mode="overwrite")

    con.close()

    logger.info(f"[lakehouse] Silver layer created at: {silver_path}")

if __name__ == "__main__":
    load_silver()