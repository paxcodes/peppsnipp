from os import getenv

from dotenv import load_dotenv

from peppcrawler import PepperplateCrawler
from utils import askFormat
from utils import getRecipeLinks

load_dotenv()
kPepperplateEmail = getenv("PEPPERPLATE_EMAIL")
kPepperplatePw = getenv("PEPPERPLATE_PW")
format = askFormat()

crawler = PepperplateCrawler()
crawler.Login(kPepperplateEmail, kPepperplatePw)
recipeLinks = getRecipeLinks(crawler)
crawler.ProcessRecipeLinks(format)

crawler.quitDriver()
