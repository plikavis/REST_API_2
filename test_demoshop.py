import allure
import selene
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from requests import Response
from selene.support.conditions import have
from selene.support.shared import browser

BASE_URL = "https://demowebshop.tricentis.com/"


def test_add_item_api_main_page():
    with step("Get cookie"):
        cookie = browser.driver.get_cookie("NOPCOMMERCE.AUTH")
    with step("Add product"):
        result: Response = requests.post(url=BASE_URL + 'addproducttocart/details/75/1',
                                         data={'product_attribute_75_5_31': 96,
                                               'product_attribute_75_6_32': 100,
                                               'product_attribute_75_3_33': 102,
                                               'addtocart_75.EnteredQuantity': 1},
                                         cookies={"NOPCOMMERCE.AUTH": cookie["value"]}
                                         )
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")
    with step('Check shopping cart'):
        browser.open('https://demowebshop.tricentis.com/cart')
        browser.element('.product-subtotal').should(have.text('800.00'))
        browser.element('.product-name').should(have.text('Simple Computer'))


def test_add_books():
    cookie = browser.driver.get_cookie("NOPCOMMERCE.AUTH")
    result: Response = requests.post(url=BASE_URL + 'addproducttocart/catalog/45/1/1',
                                     cookies={"NOPCOMMERCE.AUTH": cookie["value"]}
                                     )
    allure.attach(body=str(result.request.url), name="Request URL", attachment_type=AttachmentType.TEXT, extension="txt")
    allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
    allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")
    browser.open('https://demowebshop.tricentis.com/cart')
    browser.element('.product-subtotal').should(have.text('24.00'))
    browser.element('.product-name').should(have.text('Fiction'))
