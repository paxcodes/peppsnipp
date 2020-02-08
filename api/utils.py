from os import path

import json
import unicodedata
import re

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


def getRecipeLinks(crawler):
    if path.exists(pathToRecipeLinks):
        with open(pathToRecipeLinks, "r") as f:
            return json.load(f)
    else:
        recipeLinks = crawler.FetchRecipeLinks()
        saveRecipeLinks(recipeLinks)
        return recipeLinks


def askFormat():
    while True:
        format = input(
            "What format would you like:\n[j]son\n[p]ng screenshots\n[b]oth\n>> ")
        format = format.strip()
        if format in "jbp":
            return format
        else:
            print("Enter `j` for JSON, `p` for PDF, `b` for both.")
