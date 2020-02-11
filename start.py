from os import getenv

from peppcrawler import PepperplateCrawler
from utils import askFormat
from utils import getRecipeLinks
from utils import createDirectories

createDirectories()
format = askFormat()
crawler = PepperplateCrawler()
crawler.visitLoginPage()

while True:
    kPepperplateEmail = input("Pepperplate Email: ")
    kPepperplatePw = input("Pepperplate Password: ")
    successful, message = crawler.loginToPepperplate(
        kPepperplateEmail, kPepperplatePw)
    if successful:
        break
    else:
        print(message)

recipeLinks, message = getRecipeLinks(crawler)
crawler.ProcessRecipeLinks(recipeLinks, format)

crawler.quitDriver()
