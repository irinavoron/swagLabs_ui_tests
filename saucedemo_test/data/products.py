from dataclasses import dataclass
from selene import browser


@dataclass
class Product:
    name: str
    price: str
    add_id: str
    remove_id: str


backpack = Product(
    name='Sauce Labs Backpack',
    price='29.99',
    add_id='#add-to-cart-sauce-labs-backpack',
    remove_id='#remove-sauce-labs-backpack'
)

bike_light = Product(
    name='Sauce Labs Bike Light',
    price='9.99',
    add_id='#add-to-cart-sauce-labs-bike-light',
    remove_id='#remove-sauce-labs-bike-light'
)
