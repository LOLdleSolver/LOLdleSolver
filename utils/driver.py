import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.wait import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.enums import Results, Categories



class Driver:
    def __init__(self):
        # Setup
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

        self.driver = driver

        driver.get("http://www.loldle.net")


        # Click button
        button = driver.find_element(By.CLASS_NAME, "button-img")
        button.click()

        try:
            self.input = Wait(self.driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type champion name ...']")))
        
        except TimeoutException:
            print("Loading took to long...")
            return


        # Disable CSS animations
        # self.driver.execute_script("document.documentElement.style.setProperty('--animate-duration', 0)")


        if self.input and self.driver:
            self.ready = True

    def check_for_victory(self) -> bool:
        try:
            return self.driver.find_element(By.CLASS_NAME, "background-end") != None
        
        except:
            return False

    def input_champ(self, champ: str):
        if not self.ready:
            return

        try:
            self.input.send_keys(champ + Keys.ENTER)
        except:
            return None

        time.sleep(5)

        row = self.driver.find_element(By.CLASS_NAME, "answers-container").find_elements(By.CLASS_NAME, "classic-answer")[-1]
        squares = row.find_element(By.CLASS_NAME, "square-container").find_elements(By.CLASS_NAME, "square")
        
        del squares[0]

        result = {}

        for category, i in zip(Categories, range(7)):
            result[category.value] = self._parse_element_classes(squares[i])

        return result


    def _parse_element_classes(self, element) -> Results:
        if "square-good" in element.get_attribute("class"):
            return Results.GOOD

        elif "square-partial" in element.get_attribute("class"):
            return Results.PARTIAL

        elif "square-bad" in element.get_attribute("class"):
            return Results.BAD

        elif "square-superior" in element.get_attribute("class"):
            return Results.SUPERIOR
        
        elif "square-inferior" in element.get_attribute("class"):
            return Results.INFERIOR

        else:
            print("Kellek-Fehler")
            return None  # type: ignore
