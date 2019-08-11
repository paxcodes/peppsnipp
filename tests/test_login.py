import os
import pytest
from settings import load as loadSettings
from PepperplateCrawler import PepperplateCrawler

@pytest.fixture()
def crawler():
  crawler = PepperplateCrawler()
  return crawler

def test_canVisitLoginPage(crawler):
  response = crawler.visitLoginPage()
  crawler.quitDriver()
  assert response['title'] == 'Pepperplate'
  
def test_canLoginToPepperplate(crawler):
  loadSettings()
  email = os.getenv("PEPPERPLATE_EMAIL")
  password = os.getenv("PEPPERPLATE_PW")
  crawler.visitLoginPage()
  recipe_total = crawler.loginToPepperplate(email, password)
  crawler.quitDriver()
  
  assert recipe_total == '315 RECIPES'
  