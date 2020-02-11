from os import path
from os import mkdir

import json
import unicodedata
import re

from definitions import PYTHON_APP_DIR

pathToRecipeLinks = path.join(PYTHON_APP_DIR, "output", "_recipeLinks.json")
pepperplateDir = "~/Pepperplate"


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


prevSlug = ""
suffix = 2


def generateFileName(title):
    global prevSlug, suffix
    fileName = slugify(title)
    if fileName == prevSlug:
        fileName = f"{fileName}{suffix}"
        suffix += 1
    else:
        prevSlug = fileName
        suffix = 2

    return fileName


def saveRecipeAsJson(recipe, fileName):
    with open(path.join(path.expanduser(pepperplateDir), "j", f"{fileName}.json"), "a") as f:
        json.dump(recipe, f, indent=3)


def saveRecipeLinks(links):
    with open(pathToRecipeLinks, "a") as f:
        json.dump(links, f, indent=3)


def createDirectories():
    print("Creating folders in ~/Pepperplate...")
    createDirectory(['~', "Pepperplate"])
    createDirectory(['~', "Pepperplate", "j"])
    createDirectory(['~', "Pepperplate", "p"])


def createDirectory(pathPieces):
    try:
        mkdir(path.expanduser('/'.join(pathPieces)))
        print(f"Directory {'/'.join(pathPieces)} created!")
    except FileExistsError:
        print(f"Directory {'/'.join(pathPieces)} already exists!")


def getRecipeLinks(crawler):
    if path.exists(pathToRecipeLinks):
        with open(pathToRecipeLinks, "r") as f:
            return json.load(f), "Recipe Links have already been scraped!"
    else:
        recipeLinks = crawler.FetchRecipeLinks()
        saveRecipeLinks(recipeLinks)
        return recipeLinks, "Finished scraping recipe links!"


def askFormat():
    while True:
        format = input(
            "What export format would you like:\n[j]son\n[p]ng screenshots\n[b]oth\n>> ")
        format = format.strip()
        if format in "jbp":
            return format
        else:
            print("Enter `j` for JSON, `p` for PDF, `b` for both.")
