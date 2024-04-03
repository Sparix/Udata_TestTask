import types
from dataclasses import dataclass
from typing import Optional, Type
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "https://www.mcdonalds.com/"
endpoint_menu = "ua/uk-ua/eat/fullmenu.html"


@dataclass
class Product:
    name: str
    description: str
    calories: str
    fats: str
    carbs: str
    proteins: str
    unsaturated: str
    sugar: str
    salt: str
    portion: str


class WebDriver:
    """
    Context manager for managing WebDriver instance.
    """

    def __init__(self, driver: webdriver) -> None:
        self.driver = driver

    def __enter__(self) -> webdriver:
        return self.driver

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[types.TracebackType]
    ) -> None:
        self.driver.quit()


def scrape_all_links(driver: webdriver) -> list[Product]:
    """
    Scrapes all product links and then scrapes detailed product information.
    """
    main_url = urljoin(BASE_URL, endpoint_menu)
    driver.get(main_url)
    links = driver.find_elements(
        By.CSS_SELECTOR, ".cmp-category__row > li.cmp-category__item > a"
    )
    links_to_follow = [link.get_attribute("href") for link in links]
    all_products = []
    for link in links_to_follow:
        driver.get(link)
        all_products.append(scrape_detail_product(driver))

    return all_products
