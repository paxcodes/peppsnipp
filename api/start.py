from os import getenv
import json

from peppcrawler import PepperplateCrawler


def saveRecipeLinks(links):
    with open("output/_recipeLinks.json", "w") as f:
        json.dump(links, f, indent=3)


kPepperplateEmail = getenv("PEPPERPLATE_EMAIL")
kPepperplatePw = getenv("PEPPERPLATE_PW")

crawler = PepperplateCrawler()
crawler.Login(kPepperplateEmail, kPepperplatePw)
recipeLinks = crawler.FetchRecipeLinks()
saveRecipeLinks(recipeLinks)

# crawler.SnipRecipes()
# @todo Use "with" so crawler is automatically quit?
crawler.quitDriver()
