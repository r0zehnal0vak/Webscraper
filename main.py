from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import re
#from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome('/path/to/chromedriver')
pageurl = "https://apl.unob.cz/StudentskeHodnoceni/Student/StatistikaPredm"
driver.get(pageurl)


# zadání autentizačních dat
source = driver.page_source # <-- breakpoint, pozastavení programu pro zadání údajů 
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

buttons = driver.find_elements(By.XPATH, "//a[@class='btn btn-default btn-xs statistikaHodnoceniPredm']")

for button in buttons:
    button.click()
    # POČKEJ, NEŽ SE NAČTE OKNO
    ps=driver.page_source
    position=ps.index("axis-y")-20
    pageData=ps[position-20:position+5000] # vezme kus kódu ze stránky ve stanoveném rozmezí
    #print(pageData)
    pattern = r'<*"0" dy="0.32em">(.*?)<'
    #pattern2 = r'<*"0" dy="1.4200000000000002em">(.*?)<'
    tspan_elements = re.findall(pattern, pageData)
    print(tspan_elements)

    for tspan_element in tspan_elements:
        order, name = tspan_element.split(". ")
        print(order)
        print(name)
        data.append({
            'name': name,
            'order': order
        })
        #print(tspan_element)

    closeButton = driver.find_element(By.XPATH, "//a[@class='close']")
    closeButton.click()


driver.close()

import json

output_file = "data.json" 
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False)