from collections import OrderedDict
from os import getenv
from pathlib import Path
import json

import pytest

from peppcrawler import PepperplateCrawler
from definitions import PYTHON_APP_DIR

recipeLink = "https://www.pepperplate.com/recipes/view.aspx?id=16244702"
expectedRecipeJsonFile = Path(
    PYTHON_APP_DIR, "tests/peppcrawler/fixture/expectedRecipe.json"
)

with open(expectedRecipeJsonFile, 'r') as jsonFile:
    expectedRecipe = OrderedDict(json.load(jsonFile))


@pytest.fixture(scope="module")
def scraper():
    crawler = PepperplateCrawler()
    email = getenv("PEPPERPLATE_EMAIL")
    password = getenv("PEPPERPLATE_PW")
    crawler.Login(email, password)
    crawler.driver.get(recipeLink)
    return crawler.recipeScraper


def test_scrapeTitle(scraper):
    actualTitle = scraper.Title()
    assert expectedRecipe["title"] == actualTitle


def test_scrapeSource(scraper):
    actualSource = scraper.Source()
    assert expectedRecipe["source"] == actualSource


def test_scrapeDescription(scraper):
    actualDescription = scraper.Description()
    assert expectedRecipe["description"] == actualDescription


def test_scrapeYield(scraper):
    actualYield = scraper.Yield()
    assert expectedRecipe["yield"] == actualYield


def test_scrapeActiveTime(scraper):
    actualActiveTime = scraper.ActiveTime()
    assert expectedRecipe["active_time"] == actualActiveTime


def test_scrapeTotalTime(scraper):
    actualTotalTime = scraper.TotalTime()
    assert expectedRecipe["total_time"] == actualTotalTime


def test_scrapeCategories(scraper):
    actualCategories = scraper.Categories()
    assert expectedRecipe["categories"] == actualCategories


def test_scrapeImageSrc(scraper):
    actualImageSrc = scraper.Image()
    assert expectedRecipe["image"] == actualImageSrc


def test_scrapeNotes(scraper):
    actualNotes = scraper.Notes()
    assert expectedRecipe["notes"] == actualNotes


def test_scrapeIngredients(scraper):
    actualIngredients = scraper.Ingredients()
    assert expectedRecipe["ingredients"] == actualIngredients


def test_scrapeInstructions(scraper):
    actualInstructions = scraper.Instructions()
    assert expectedRecipe["instructions"] == actualInstructions
