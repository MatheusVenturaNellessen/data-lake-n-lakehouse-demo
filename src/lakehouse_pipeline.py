import logging

from lakehouse_01_bronze import load_bronze
from lakehouse_02_silver import load_silver
from lakehouse_03_gold import load_gold

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        load_bronze()
        load_silver()
        load_gold()

    except Exception:
        logger.exception(f"[lakehouse] Pipeline failed")
        raise