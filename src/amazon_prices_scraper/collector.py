"""
    Main module for collecting Amazon prices.
"""

import logging

from typing import List

import pandas as pd

from amazon_prices_scraper.models import Product
from amazon_prices_scraper.scraper import AmazonPriceScraper


DEFAULT_OUTPUT_FILE = "amazon_prices.csv"


class AmazonDataCollector:
    """Data collector class for Amazon pages"""

    def __init__(
        self,
        output_file: str | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self._scraper = AmazonPriceScraper()
        self._output_file = output_file if output_file else DEFAULT_OUTPUT_FILE
        self._logger = logger if logger else logging.getLogger(__name__)

    def _save_to_csv(self, products: List[Product]) -> None:
        """Saves given list of products with prices to a CSV file."""
        self._logger.info(f"Writing {len(products)} products to {self._output_file}..")
        product_objects = [product.model_dump() for product in products]
        df = pd.DataFrame(product_objects)
        df.to_csv(self._output_file)

    def collect_amazon_price_data(self, url: str) -> None:
        """
        Scrapes price data from a given Amazon page and stores it into a CSV file.

        Args:
            url (str): The URL of the Amazon page for which to scrape price data.
        """
        self._logger.info(f"Getting Amazon prices for url {url}..")
        try:
            products = self._scraper.scrape_amazon_prices(url)
        except Exception:
            self._logger.exception(f"Error when scraping Amazon prices for url {url}.")
            return

        if not products:
            self._logger.info("No prices found for given Amazon page.")
            return

        self._save_to_csv(products)
