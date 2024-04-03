import types
from dataclasses import dataclass
from typing import Optional, Type

from selenium import webdriver


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
