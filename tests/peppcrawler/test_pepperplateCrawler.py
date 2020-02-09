from collections import OrderedDict
from os import getenv
from pathlib import Path
import json

from peppcrawler import PepperplateCrawler
from definitions import PYTHON_APP_DIR

recipeLink = "https://www.pepperplate.com/recipes/view.aspx?id=16244702"
expectedRecipeJsonFile = Path(
    PYTHON_APP_DIR, "tests/peppcrawler/fixture/expectedRecipe.json"
)

with open(expectedRecipeJsonFile, 'r') as jsonFile:
    expectedRecipe = OrderedDict(json.load(jsonFile))


def test_scrapeRecipePage():
    crawler = PepperplateCrawler()
    email = getenv("PEPPERPLATE_EMAIL")
    password = getenv("PEPPERPLATE_PW")
    crawler.Login(email, password)
    actualRecipe = crawler.ScrapeRecipePage(recipeLink)
    assert actualRecipe == expectedRecipe
