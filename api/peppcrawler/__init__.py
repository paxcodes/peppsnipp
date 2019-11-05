import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv


class PepperplateCrawler:
    loginURL = "https://www.pepperplate.com/login.aspx"

    def __init__(self):
        load_dotenv()
        self.startDriver()

    def startDriver(self):
        options = Options()
        options.headless = True
        print('Browser: Starting...')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.driver = webdriver.Firefox(
            options=options, executable_path=dir_path + '/geckodriver/' + os.getenv("OS"))
        self.driver.set_window_size(1080, 800)
        self.driver.implicitly_wait(10)
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


    def __AcceptCookies(self):
        try:
            element = self.driver.find_element_by_xpath(
                "//button[@class='sd-cmp-ieaP1']")
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
