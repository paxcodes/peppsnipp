import pytest
from PepperplateCrawler import PepperplateCrawler

@pytest.fixture()
def crawler():
  crawler = PepperplateCrawler()
  return crawler

def test_canVisitLoginPage(crawler):
  response = crawler.visitLoginPage()
  crawler.quitDriver()
  assert response['title'] == 'Pepperplate'
  