from os import getenv
from os import path
import json
import unicodedata
import re

from dotenv import load_dotenv

from peppcrawler import PepperplateCrawler

pathToRecipeLinks = "output/_recipeLinks.json"


def slugify(value):
    """
    Convert to ASCII. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode(
        'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s]', '', value).strip()
    return re.sub(r'[-\s]+', '', value.title())


def generateFileName(title, format):
    fileName = slugify(title)
    suffix = 2
    while True:
        if not path.exists(path.join("output", format, f"{fileName}.json")):
            return fileName
        else:
            fileName = f"{fileName}{suffix}"
            suffix += 1


def saveRecipe(recipe, format=""):
    fileName = generateFileName(recipe["title"], format)
    with open(path.join("output", format, f"{fileName}.json"), "a") as f:
        json.dump(recipe, f, indent=3)


def saveRecipeLinks(links):
    with open(pathToRecipeLinks, "a") as f:
        json.dump(links, f, indent=3)


def getRecipeLinks():
    with open(pathToRecipeLinks, "r") as f:
        return json.load(f)


load_dotenv()
kPepperplateEmail = getenv("PEPPERPLATE_EMAIL")
kPepperplatePw = getenv("PEPPERPLATE_PW")

crawler = PepperplateCrawler()
crawler.Login(kPepperplateEmail, kPepperplatePw)

if not path.exists(pathToRecipeLinks):
    recipeLinks = crawler.FetchRecipeLinks()
    saveRecipeLinks(recipeLinks)
else:
    recipeLinks = getRecipeLinks()

for recipeLink in recipeLinks:
    recipe = crawler.ScrapeRecipePage(recipeLink)
    saveRecipe(recipe)

# @todo Use "with" so crawler is automatically quit?
crawler.quitDriver()
