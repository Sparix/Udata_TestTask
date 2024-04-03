import json
import time
import types
from dataclasses import dataclass, asdict
from typing import Optional, Type
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from slugify import slugify

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


def parse_product(driver: webdriver):
    """
    Parses product information from the product detail page.
    """
    time.sleep(0.5)
    detail_info = driver.find_elements(
        By.CSS_SELECTOR,
        "ul.cmp-nutrition-summary__heading-primary > "
        "li.cmp-nutrition-summary__heading-primary-item"
    )
    secondary_nutrition = driver.find_elements(
        By.CSS_SELECTOR,
        "div.cmp-nutrition-summary__details-column-view-mobile > "
        "ul > li.label-item"
    )
    return Product(
        name=driver.find_element(By.CSS_SELECTOR, "span.cmp-product-details-main__heading-title").text.replace("®", ""),
        description=driver.find_element(By.CSS_SELECTOR, "div.cmp-text").text.strip(),
        calories=detail_info[0].find_elements(By.CSS_SELECTOR, "span.value > span")[2].text,
        fats=detail_info[1].find_elements(By.CSS_SELECTOR, "span.value > span")[2].text,
        carbs=detail_info[2].find_elements(By.CSS_SELECTOR, "span.value > span")[2].text,
        proteins=detail_info[3].find_elements(By.CSS_SELECTOR, "span.value > span")[2].text,
        unsaturated=secondary_nutrition[0].find_elements(By.CSS_SELECTOR, "span.value > span")[0].text,
        sugar=secondary_nutrition[1].find_elements(By.CSS_SELECTOR, "span.value > span")[0].text,
        salt=secondary_nutrition[2].find_elements(By.CSS_SELECTOR, "span.value > span")[0].text,
        portion=secondary_nutrition[3].find_elements(By.CSS_SELECTOR, "span.value > span")[0].text,
    )


def scrape_detail_product(driver):
    """
    Scrapes product information from the product detail page.
    """
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "h2.cmp-accordion__header > button.cmp-accordion__button"))
    )
    ActionChains(driver).move_to_element(button).perform()
    button.click()
    return parse_product(driver)


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


def get_all_products() -> None:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    with WebDriver(webdriver.Chrome(options=options)) as driver:
        products = {slugify(product.name): asdict(product) for product in scrape_all_links(driver)}
        with open("product.json", "w", encoding="UTF-8") as json_file:
            json.dump(products, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    get_all_products()
