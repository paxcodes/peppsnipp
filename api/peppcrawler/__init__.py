import os
import time
from collections import OrderedDict

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

from peppcrawler.PeppRecipeScraper import PeppRecipeScraper
from utils import saveRecipe

driverPath = os.path.dirname(
    os.path.realpath(__file__)) + '/driver'


class PepperplateCrawler:
    loginURL = "https://www.pepperplate.com/login.aspx"
    chromeDriverPath = driverPath + '/ChromeDriver'

    def __init__(self):
        load_dotenv()
        self.driver = self.startDriver()
        self.recipeScraper = PeppRecipeScraper(self.driver)

    def startDriver(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")

        print('Browser: Starting...')
        driver = webdriver.Chrome(
            chrome_options=options, executable_path=self.chromeDriverPath)
        driver.set_window_size(1080, 800)
        print('Browser: Started!')
        return driver

    def quitDriver(self):
        print('Browser: Quitting...')
        self.driver.quit()
        print('Browser: Quit!...')

    def visitLoginPage(self):
        print('Page: Loading Login Page...')
        self.driver.get(self.loginURL)
        print('Page: Loaded!')
        return {
            "title": self.driver.title
        }

    def loginToPepperplate(self, email, password):
        self.__TypeCredentials(email, password)
        self.__AcceptCookies()

        self.driver.find_element_by_id(
            'cphMain_loginForm_ibSubmit').click()

        return True

    def Login(self, email, password):
        self.visitLoginPage()
        self.loginToPepperplate(email, password)

    def GetUsersName(self):
        name = self.driver.find_element_by_id('lblName').text
        return name

    def GetRecipeTotal(self):
        recipeTotalElem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'reclistcount')))
        recipeTotalString = recipeTotalElem.text
        return int(recipeTotalString.split()[0])

    def FetchRecipeLinks(self):
        self.driver.find_element_by_id("cphMiddle_lbSortAlpha").click()
        self.__LoadAllRecipes()
        recipeLinks = []

        anchorTags = self.driver.find_elements_by_css_selector(
            '.item > p > a')

        for i, anchorTag in enumerate(anchorTags, start=1):
            link = anchorTag.get_attribute("href")
            recipeLinks.append(link)
            print(f"{i}: {anchorTag.text} {link}")

        return recipeLinks

    def ProcessRecipeLinks(self, recipeLinks):
        pass

    def SnipRecipePages(self, recipeLinks):
        pass

    def JsonifyRecipePages(self, recipeLinks):
        for recipeLink in recipeLinks:
            recipe = self.ScrapeRecipePage(recipeLink)
            saveRecipe(recipe)

    def ScrapeRecipePage(self, recipeLink):
        self.driver.get(recipeLink)
        recipe = OrderedDict()

        recipe["title"] = self.recipeScraper.Title()
        recipe["source"] = self.recipeScraper.Source()
        recipe["description"] = self.recipeScraper.Description()
        recipe["yield"] = self.recipeScraper.Yield()
        recipe["active_time"] = self.recipeScraper.ActiveTime()
        recipe["total_time"] = self.recipeScraper.TotalTime()
        recipe["categories"] = self.recipeScraper.Categories()
        recipe["ingredients"] = self.recipeScraper.Ingredients()
        recipe["instructions"] = self.recipeScraper.Instructions()
        recipe["notes"] = self.recipeScraper.Notes()
        recipe["image"] = self.recipeScraper.Image()

        return recipe

    def __LoadAllRecipes(self):
        while True:
            try:
                loadMore = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'loadmorelink')))
            except (NoSuchElementException, TimeoutException):
                break
            else:
                self.driver.execute_script("arguments[0].click();", loadMore)
                time.sleep(2)

    def __AcceptCookies(self):
        try:
            element = self.driver.find_element_by_css_selector(
                'button.sd-cmp-ieaP1')
        except NoSuchElementException:
            pass
        else:
            element.click()

    def __TypeCredentials(self, email, password):
        email_field = self.driver.find_element_by_name(
            'ctl00$cphMain$loginForm$tbEmail')
        email_field.send_keys(email)

        password_field = self.driver.find_element_by_name(
            'ctl00$cphMain$loginForm$tbPassword')
        password_field.send_keys(password)
