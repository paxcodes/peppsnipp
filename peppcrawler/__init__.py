import os
import time
import re
from collections import OrderedDict

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from peppcrawler.PeppRecipeScraper import PeppRecipeScraper
from utils import saveRecipeAsJson
from utils import generateFileName
from utils import pepperplateDir
from definitions import PYTHON_APP_DIR

driverPath = os.path.dirname(
    os.path.realpath(__file__)) + '/driver'


class PepperplateCrawler:
    loginURL = "https://www.pepperplate.com/login.aspx"
    chromeDriverPath = driverPath + '/ChromeDriver'

    def __init__(self):
        self.driver = self.startDriver()
        self.recipeScraper = PeppRecipeScraper(self.driver)

    def startDriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

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
        self.__Log('🌏 Loading `Pepperplate` Login Page...')
        self.driver.get(self.loginURL)
        self.__Log('🌏 `Pepperplate` Login Page Loaded!')
        self.__Log('Enter your credentials in the form above ⬆️')
        return {
            "title": self.driver.title
        }

    def loginToPepperplate(self, email, password):
        self.__Log("⌨️ Entering login credentials...")
        self.__TypeCredentials(email, password)
        self.__AcceptCookies()

        self.__Log("⌨️ Submitting credentials...")
        self.driver.find_element_by_id(
            'cphMain_loginForm_ibSubmit').click()

        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'lblName')))
        except TimeoutException:
            message = self.__GetErrorMessage()
            return False, f"🛑 {message}"
        else:
            return True, "Success!"

    def __GetErrorMessage(self):
        errorsContainer = self.driver.find_element_by_class_name("errors")
        return errorsContainer.find_element_by_xpath("descendant::li").text

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
        self.__Log(f"✨1 Fetching recipe links...")
        self.driver.find_element_by_id("cphMiddle_lbSortAlpha").click()
        self.__LoadAllRecipes()
        recipeLinks = []

        anchorTags = self.driver.find_elements_by_css_selector(
            '.item > p > a')

        for i, anchorTag in enumerate(anchorTags, start=1):
            link = anchorTag.get_attribute("href")
            recipeLinks.append(link)
            self.__Log(f"{i}: {anchorTag.text} {link}")

        return recipeLinks

    def ProcessRecipeLinks(self, recipeLinks, format):
        totalRecipes = len(recipeLinks)
        for i, recipeLink in enumerate(recipeLinks, start=1):
            self.__Log(f"🌏 {i}/{totalRecipes}: Loading recipe page...")
            self.driver.get(recipeLink)
            title = re.sub(r'^Pepperplate - ', '', self.driver.title)
            self.__Log(f"🕜 {i}/{totalRecipes}: Exporting {title}...")
            fileName = generateFileName(title)
            if format in 'jb':
                recipe = self.ScrapeRecipePage()
                saveRecipeAsJson(recipe, fileName)

            if format in 'pb':
                self.__GetFullScreenshot(fileName)

            self.__Log(f"✅ {i}/{totalRecipes}: Exported {title}")

    def __GetFullScreenshot(self, fileName):
        path = os.path.join(os.path.expanduser(
            pepperplateDir), "p", f"{fileName}.png")
        requiredWidth = self.driver.execute_script(
            'return document.body.parentNode.scrollWidth')
        requiredHeight = self.driver.execute_script(
            'return document.body.parentNode.scrollHeight')
        self.driver.set_window_size(requiredWidth, requiredHeight)
        self.driver.find_element_by_class_name('recipedet').screenshot(path)

    def ScrapeRecipePage(self, recipeLink=""):
        if recipeLink != "":
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
        counter = 2
        while True:
            try:
                loadMore = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'loadmorelink')))
            except (NoSuchElementException, TimeoutException):
                break
            else:
                self.driver.execute_script("arguments[0].click();", loadMore)
                self.__Log(f"✨{counter} Fetching more recipe links...")
                counter += 1
                time.sleep(1)

    def __AcceptCookies(self):
        try:
            element = self.driver.find_element_by_css_selector(
                'button.sd-cmp-ieaP1')
        except NoSuchElementException:
            pass
        else:
            element.click()

    def __TypeCredentials(self, email, password):
        email_field = self.driver.find_element_by_id(
            'cphMain_loginForm_tbEmail')
        email_field.clear()
        email_field.send_keys(email)

        password_field = self.driver.find_element_by_id(
            'cphMain_loginForm_tbPassword')
        password_field.clear()
        password_field.send_keys(password)

    def SetForm(self, form):
        self.form = form

    def __Log(self, message):
        if hasattr(self, 'form'):
            self.form.Log(message)
        else:
            print(message)
