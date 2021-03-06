import re

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
        return self.__GetTextElementById("cphMiddle_cphMain_lblTotalTime")

    def Categories(self):
        text = self.__GetTextElementById("cphMiddle_cphMain_pnlTags")
        return re.sub(r'^CATEGORIES ', '', text)

    def Ingredients(self):
        ingredients = []
        try:
            ingredientGroups = self.driver.find_elements_by_class_name(
                "inggroupitems")
        except NoSuchElementException:
            return ingredients
        else:
            for ingredientGroup in ingredientGroups:
                label = self.__GetGroupLabel(ingredientGroup)
                items = self.__GetIngredientItems(ingredientGroup)
                ingredients.append({
                    "group_name": label,
                    "list": items
                })

        return ingredients

    def Instructions(self):
        instructions = []
        try:
            instructionGroups = self.driver.find_elements_by_class_name(
                "dirgroupitems")
        except NoSuchElementException:
            return instructions
        else:
            for instructionGroup in instructionGroups:
                label = self.__GetGroupLabel(instructionGroup)
                steps = self.__GetSteps(instructionGroup)
                instructions.append({
                    "group_name": label,
                    "steps": steps
                })

        return instructions

    def Notes(self):
        return self.__GetTextElementById("cphMiddle_cphMain_lblNotes")

    def Image(self):
        try:
            element = self.driver.find_element_by_id(
                "cphMiddle_cphMain_imgRecipeThumb")
        except NoSuchElementException:
            return ""
        else:
            src = element.get_attribute("src")
            src = re.sub(r'\?preset=sitethumb$', '', src)
            return src

    def __GetTextElementById(self, id):
        try:
            textElement = self.driver.find_element_by_id(id)
        except NoSuchElementException:
            return ""
        else:
            return textElement.text

    def __GetGroupLabel(self, groupElement):
        try:
            labelElement = groupElement.find_element_by_xpath(
                "preceding-sibling::h4")
        except NoSuchElementException:
            return ""
        else:
            return labelElement.text

    def __GetIngredientItems(self, ingredientGroup):
        items = []
        itemElements = ingredientGroup.find_elements_by_class_name("item")
        for itemElement in itemElements:
            quantity = itemElement.find_element_by_class_name(
                "ingquantity").text
            item = itemElement.find_element_by_class_name("content").text
            if quantity != "":
                item = re.sub(rf'{quantity} ?', '', item)

            items.append({"quantity": quantity, "item": item})
        return items

    def __GetSteps(self, instructionGroup):
        steps = []
        stepElements = instructionGroup.find_elements_by_class_name("text")

        for stepElement in stepElements:
            step = stepElement.text
            steps.append(step)

        return steps
