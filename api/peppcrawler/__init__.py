import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

driverPath = os.path.dirname(
    os.path.realpath(__file__)) + '/driver'


class PepperplateCrawler:
    loginURL = "https://www.pepperplate.com/login.aspx"
    chromeDriverPath = driverPath + '/ChromeDriver'
    browserAppPath = driverPath + '/Brave Browser.app/Contents/MacOS/Brave Browser'

    def __init__(self):
        load_dotenv()
        self.startDriver()

    def startDriver(self):
        options = webdriver.ChromeOptions()
        options.binary_location = self.browserAppPath
        # options.add_argument("--headless")

        print('Browser: Starting...')
        self.driver = webdriver.Chrome(
            chrome_options=options, executable_path=self.chromeDriverPath)
        self.driver.set_window_size(1080, 800)
        print('Browser: Started!')

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
        while True:
            try:
                loadMore = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'loadmorelink')))
            except NoSuchElementException:
                break
            else:
                loadMore.click()

        recipeLinks = []

        anchorTags = self.driver.find_elements_by_css_selector(
            '.item > p > a')

        for i, anchorTag in enumerate(anchorTags, start=1):
            link = anchorTag.getAttribute("href")
            recipeLinks.append(link)
            print(f"{i}: {anchorTag.LinkText}  {link}")

        return recipeLinks

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
