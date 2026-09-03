import logging

from lake_01_bronze import load_bronze
from lake_02_silver import load_silver
from lake_03_gold import load_gold

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
        logger.exception("[lake] Pipeline failed")
        raise