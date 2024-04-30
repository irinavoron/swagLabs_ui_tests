import os

import allure
from selene import browser, be, have
import pytest
from dotenv import load_dotenv

from saucedemo_test.data import products
from saucedemo_test.pages import login_page, common
from saucedemo_test.pages.common import select_product, product_details_match_selected_product
from saucedemo_test.pages.inventory_page import InventoryPage
from saucedemo_test.pages.cart_page import Cart

inventory_page = InventoryPage()
cart = Cart()

load_dotenv()
user_name = os.getenv('USER_NAME')
user_password = os.getenv('USER_PASSWORD')


def test_successful_login():
    login_page.successful_login()

    with allure.step('The catalogue is opened after logging in'):
        browser.element('.inventory_list').should(be.visible)


@pytest.mark.parametrize(
    'login, password', [
        ('wrong_name', {user_password}),
        ({user_name}, 'wrong_password'),
        ('', ''),
        ('locked_out_user', {user_password})
    ],
    ids=['invalid name', 'invalid password', 'empty form', 'locked out user']
)
def test_unsuccessful_login(login, password):
    login_page.unsuccessful_login(login, password)

    with allure.step('Verify that error message is displayed'):
        browser.element('.error-button').should(be.visible)


def test_cart_badge_displays_items_number():
    login_page.successful_login()
    inventory_page.add_product_to_cart(products.backpack)

    with allure.step('The cart badge shows number of added items - 1'):
        browser.element('.shopping_cart_badge').should(have.text('1'))

    inventory_page.add_product_to_cart(products.bike_light)

    with allure.step('The cart badge shows number of added items - 2'):
        browser.element('.shopping_cart_badge').should(have.text('2'))

    cart.clear_cart(2)


def test_product_is_added_to_cart():
    login_page.successful_login()
    inventory_page.add_product_to_cart(products.backpack)
    inventory_page.open_cart()

    product_details_match_selected_product(products.backpack)

    cart.clear_cart(1)


def test_product_page_can_be_opened_from_inventory_page():
    login_page.successful_login()

    select_product(products.bike_light)

    product_details_match_selected_product(products.bike_light)


def test_product_can_be_removed_from_cart():
    login_page.successful_login()
    inventory_page.add_product_to_cart(products.backpack)
    inventory_page.open_cart()

    cart.remove_product(products.backpack)

    items_list = browser.all('.cart_item')
    with allure.step('Verify the cart is empty'):
        items_list.should(have.size(0))


def test_user_can_proceed_to_checkout():
    login_page.successful_login()
    inventory_page.add_product_to_cart(products.backpack)
    inventory_page.open_cart()

    with allure.step('Click "checkout" button'):
        browser.element('#checkout').click()

    with allure.step('Verify that checkout page is opened'):
        browser.element('[data-test=title]').should(have.text('Checkout: Your Information'))

    cart.clear_cart(1)


def test_user_can_continue_shopping_from_cart():
    login_page.successful_login()
    inventory_page.add_product_to_cart(products.backpack)
    inventory_page.open_cart()

    with allure.step('Click "checkout" button'):
        browser.element('#continue-shopping').click()

    with allure.step('Verify that catalogue page is opened'):
        browser.element('.inventory_list').should(be.visible)

    cart.clear_cart(1)


def test_cart_persistence():
    login_page.successful_login()
    inventory_page.add_product_to_cart(products.backpack)
    inventory_page.open_cart()

    common.select_product(products.backpack)
    with allure.step('Go back to cart from the product page'):
        browser.element('#shopping_cart_container').click()

    common.product_details_match_selected_product(products.backpack)

    cart.clear_cart(1)
