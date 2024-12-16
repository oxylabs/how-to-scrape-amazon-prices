"""
    Pydantic models for Amazon Price scraper.
"""

from pydantic import BaseModel


class Product(BaseModel):
    title: str
    url: str
    price: str
    currency: str
