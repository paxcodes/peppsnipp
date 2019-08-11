import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from settings import load as loadSettings

class PepperplateCrawler:
  loginURL = "https://www.pepperplate.com/login.aspx"
  
  def __init__(self):
    loadSettings()
    self.startDriver()
    
  def startDriver(self):
    options = Options()
    options.headless = True
    print('Browser: Starting...')
    self.driver = webdriver.Firefox(options=options, executable_path='geckodriver/' + os.getenv("OS"))
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

  