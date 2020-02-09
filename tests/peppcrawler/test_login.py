import pytest
from os import getenv
from dotenv import load_dotenv

from peppcrawler import PepperplateCrawler


@pytest.fixture()
def crawler():
    crawler = PepperplateCrawler()
    return crawler


def test_canVisitLoginPage(crawler):
    response = crawler.visitLoginPage()
    crawler.quitDriver()
    assert response['title'] == 'Pepperplate'


def test_canLoginToPepperplate(crawler):
    load_dotenv()
    email = getenv("PEPPERPLATE_EMAIL")
    password = getenv("PEPPERPLATE_PW")
    crawler.visitLoginPage()
    success = crawler.loginToPepperplate(email, password)
    crawler.quitDriver()

    assert True == success
