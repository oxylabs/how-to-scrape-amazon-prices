"""
    Module for scraping Amazon prices.
"""

import logging
import time

from enum import Enum
from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

from seleniumwire import webdriver
from seleniumwire.request import Request

from amazon_prices_scraper.models import Product


logging.getLogger("WDM").setLevel(logging.ERROR)
logging.getLogger("seleniumwire").setLevel(logging.ERROR)


class DriverInitializationError(BaseException):
    message = "Unable to initialize Chrome webdriver for scraping."


class DriverGetProductsError(BaseException):
    message = "Unable to get Amazon product price data with Chrome webdriver."


class ProductXPath(str, Enum):
    PRODUCTS = "//div[@data-component-type='s-search-result']"
    TITLE = ".//h2[@class='a-size-base-plus a-spacing-none a-color-base a-text-normal']/span"
    URL = ".//a[@class='a-link-normal s-no-outline']"
    PRICE = ".//span[@class='a-price']"


class AmazonPriceScraper:
    """Class for scraping Amazon prices"""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger if logger else logging.getLogger(__name__)
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
            "Referer": "https://www.amazon.com/",
            "Host": "www.amazon.com",
            "TE": "Trailers",
        }

    def _add_headers_to_request(self, request: Request) -> None:
        """Intercepts selenium requests to add headers"""
        for key, value in self._headers.items():
            request.headers[key] = value

    def _init_chrome_driver(self) -> webdriver.Chrome:
        """Initializes Chrome webdriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.request_interceptor = self._add_headers_to_request
        return driver

    def _parse_price_for_product(self, price_element: WebElement) -> str | None:
        """Parses price for a product element"""
        price_whole_element = price_element.find_element(By.CLASS_NAME, "a-price-whole")
        price_whole = price_whole_element.text if price_whole_element else None

        price_fractional_element = price_element.find_element(
            By.CLASS_NAME, "a-price-fraction"
        )
        price_fractional = (
            price_fractional_element.text if price_fractional_element else None
        )
        return price_whole + "." + price_fractional

    def _parse_product_price_data(self, product: WebElement) -> Product | None:
        """Parses product price data from the given product element"""
        title_element = product.find_element(By.XPATH, ProductXPath.TITLE)
        title = title_element.text if title_element else None

        url_element = product.find_element(By.XPATH, ProductXPath.URL)
        url = url_element.get_attribute("href") if url_element else None

        try:
            price_element = product.find_element(By.XPATH, ProductXPath.PRICE)
        except NoSuchElementException:
            self._logger.warning(
                f"Price not found for product {title}. Likely out of stock."
            )
            return None

        price = self._parse_price_for_product(price_element)

        currency_element = price_element.find_element(By.CLASS_NAME, "a-price-symbol")
        currency = currency_element.text if currency_element else None

        return Product(title=title, url=url, price=price, currency=currency)

    def _get_product_prices_from_page(
        self, url: str, driver: webdriver.Chrome
    ) -> List[Product]:
        """Scrapes the Amazon page for product price"""
        driver.get(url)
        time.sleep(3)
        product_elements = driver.find_elements(By.XPATH, ProductXPath.PRODUCTS)
        parsed_products = []
        for product in product_elements:
            try:
                parsed_product = self._parse_product_price_data(product)
            except Exception:
                self._logger.exception(
                    "Uexpected error when parsing prices for product. Skipping.."
                )
                continue
            else:
                if parsed_product:
                    parsed_products.append(parsed_product)

        return parsed_products

    def scrape_amazon_prices(self, url: str) -> List[Product]:
        """
        Retrieves a list of products with prices from Amazon for a given Amazon page URL.

        Returns:
            List[Product]: A list of Product objects.
        Raises:
            DriverInitializationError: If the Chrome webdriver cannot be initialized.
            DriverGetProductsError: If the Amazon price data cannot be scraped from the Amazon site.
        """
        self._logger.info("Scraping Amazon product data..")

        try:
            driver = self._init_chrome_driver()
        except Exception as e:
            raise DriverInitializationError from e

        try:
            return self._get_product_prices_from_page(url, driver)
        except Exception as e:
            raise DriverGetProductsError from e
        finally:
            driver.close()
