import duckdb
import os
import logging

logger = logging.getLogger(__name__)

def load_gold():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    silver_path = os.path.join(base_dir, 'data', 'lake', '02_silver')
    gold_path = os.path.join(base_dir, 'data', 'lake', '03_gold')

    os.makedirs(gold_path, exist_ok=True)
    con = duckdb.connect()

    # Revenue by Country
    logger.info(f"[lake] Creating revenue_by_country at: {os.path.join(gold_path, 'revenue_by_country.parquet')}...")

    con.execute(f"""
        COPY (
            SELECT    dc.country,
                      ROUND(SUM(fs.quantity * dp.unit_price), 2)                          AS total_revenue
            FROM      read_parquet('{os.path.join(silver_path, 'fact_sales.parquet')}')   AS fs
            LEFT JOIN read_parquet('{os.path.join(silver_path, 'dim_product.parquet')}')  AS dp
                ON    fs.stock_code = dp.stock_code
            LEFT JOIN read_parquet('{os.path.join(silver_path, 'dim_customer.parquet')}') AS dc
                ON    fs.customer_id = dc.customer_id
            GROUP BY  1
            ORDER BY  2 DESC
        ) TO '{os.path.join(gold_path, 'revenue_by_country.parquet')}' (FORMAT PARQUET)
    """)

    con.close()

    logger.info(f"[lake] Gold layer created at:{gold_path}")

if __name__ == "__main__":
    load_gold()
