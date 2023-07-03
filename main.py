# print("hello world")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import re
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome('/path/to/chromedriver')
pageurl = "https://apl.unob.cz/StudentskeHodnoceni/Student/StatistikaPredm"
driver.get(pageurl)

#assert "Python" in driver.title

# zadání autentizačních dat
source = driver.page_source # vždy po spuštění kódu <-- breakpoint, pozastavení programu pro zadání údajů 
# print(source)

# choice of school year
dropdown1 = Select(driver.find_element(By.XPATH, "//*[@id='AkRokSelectList_SelectedUic']"))
dropdown1.select_by_visible_text("2020/2021")

# choice of semestr
dropdown2 = Select(driver.find_element(By.XPATH, "//*[@id='SemestrSelectList_SelectedUic']"))
dropdown2.select_by_visible_text("Zimní semestr")

# submit
submitButton = driver.find_element(By.XPATH, "//a[@class='btn btn-default btn-sm showPredmetyStatistika']")
submitButton.click()

data = []

reg = "<text([^<]*)<tspan([^>]*)>([^<]*)" 

buttons = driver.find_elements(By.XPATH, "//a[@class='btn btn-default btn-xs statistikaHodnoceniPredm']")
# print(buttons)
for button in buttons:
    button.click()
    # Zde je potřeba počkat na načtení "pop-up" okna, pak pokračovat
    dataFromButton = re.compile("<text([^<]*)<tspan([^>]*)>([^<]*)")    # TODO: scrape data for element in our DB
    data.append(dataFromButton)
    print(data)

    closeButton = driver.find_element(By.XPATH, "//a[@class='close']")
    closeButton.click()

#reg = "<text([^<]*)<tspan([^>]*)>([^<]*)" # https://regex101.com/

driver.close()

import json

output_file = "data.json"
with open(output_file, "w") as file:
    json.dump(data, file)