import allure
import pytest
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from requests import Response
from selene import have
from selene.support.shared import browser

LOGIN = "Cherry2143@yandex.ru"
PASSWORD = "123456"
API_URL = "https://demowebshop.tricentis.com/"


def clear_shopping_cart():
    with step("Clear shopping cart"):
        browser.open('https://demowebshop.tricentis.com/cart')
        browser.element('[name = "removefromcart"]').click()
        browser.element('[name ="updatecart"]').click()


@pytest.fixture(autouse=True)
def login_api():
    with step("LOGIN"):
        result = requests.post(url=API_URL + "/login",
                               data={'Email': 'Cherry2143@yandex.ru',
                                     'Password': '123456',
                                     'RememberMe': False},
                               allow_redirects=False)
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")
        cookie_auth = result.cookies.get("NOPCOMMERCE.AUTH")
        browser.open(API_URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie_auth})
        browser.open(API_URL)
        browser.element(".account").should(have.text(LOGIN))
    yield
    clear_shopping_cart()





