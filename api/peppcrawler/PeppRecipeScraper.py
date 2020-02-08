from selenium.common.exceptions import NoSuchElementException


class PeppRecipeScraper:

    def __init__(self, driver):
        self.driver = driver

    def Title(self):
        return self.driver.find_element_by_id(
            'cphMiddle_cphMain_lblTitle').text

    def Source(self):
        try:
            sourceElement = self.driver.find_element_by_id(
                'cphMiddle_cphMain_hlSource')
        except NoSuchElementException:
            return ""
        else:
            return {
                "text": sourceElement.text,
                "url": sourceElement.get_attribute("href")
            }

    def Description(self):
        return self.__GetTextElementById("cphMiddle_cphMain_lblDescription")

    def Yield(self):
        return self.__GetTextElementById("cphMiddle_cphMain_lblYield")

    def ActiveTime(self):
        return self.__GetTextElementById("cphMiddle_cphMain_lblActiveTime")

    def TotalTime(self):
        pass

    def Categories(self):
        pass

    def Ingredients(self):
        pass

    def Instructions(self):
        pass

    def Notes(self):
        pass

    def Image(self):
        pass

    def __GetTextElementById(self, id):
        try:
            textElement = self.driver.find_element_by_id(id)
        except NoSuchElementException:
            return ""
        else:
            return textElement.text
