import duckdb
import os
from deltalake import DeltaTable
from deltalake.writer import write_deltalake
import logging

logger = logging.getLogger(__name__)

def load_gold():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    silver_path = os.path.join(base_dir, 'data', 'lakehouse', '02_silver')
    gold_path = os.path.join(base_dir, 'data', 'lakehouse', '03_gold')

    con = duckdb.connect()

    dt_fact_sales = DeltaTable(os.path.join(silver_path, 'fact_sales'))
    con.register('silver_fact_sales', dt_fact_sales.to_pyarrow_dataset())

    dt_dim_product = DeltaTable(os.path.join(silver_path, 'dim_product'))
    con.register('silver_dim_product', dt_dim_product.to_pyarrow_dataset())

    dt_dim_customer = DeltaTable(os.path.join(silver_path, 'dim_customer'))
    con.register('silver_dim_customer', dt_dim_customer.to_pyarrow_dataset())

    logger.info(f"[lakehouse] Creating revenue_by_country at: {os.path.join(gold_path, 'revenue_by_country')}...")

    df_revenue_country = con.execute(f"""
        SELECT    dc.country,
                  ROUND(SUM(fs.quantity * dp.unit_price), 2) AS total_revenue
        FROM      silver_fact_sales  AS fs
        LEFT JOIN silver_dim_product AS dp
            ON    fs.stock_code = dp.stock_code
        LEFT JOIN silver_dim_customer AS dc
            ON    fs.customer_id = dc.customer_id
        GROUP BY  1
        ORDER BY  2 DESC
    """).df()
    write_deltalake(os.path.join(gold_path, 'revenue_by_country'), df_revenue_country, mode="overwrite")

    con.close()

    logger.info(f"[lakehouse] Gold layer created at: {gold_path}")

if __name__ == "__main__":
    load_gold()