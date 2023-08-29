from selenium import webdriver
#rom selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import re

#driver = webdriver.Chrome('/path/to/chromedriver')
driver = webdriver.Chrome(r'C:\Users\KRoze\Desktop\projekt\chromedriver-win64\chromedriver-win64\chromedriver.exe')
# had to download chrome driver due to the error "This version of ChromeDriver only supports Chrome version 114"
pageurl = "https://apl.unob.cz/StudentskeHodnoceni/Student/StatistikaPredm"
driver.get(pageurl)

# Intranet credentials
username = "username"
password = "password"

# zadání autentizačních dat
source = driver.page_source # <-- breakpoint, pozastavení programu pro zadání údajů 
# print(source)

driver.find_element(By.XPATH, "//*[@id='Username']").send_keys(username)
driver.find_element(By.XPATH, "//*[@id='Password']").send_keys(password)
driver.find_element(By.XPATH, "//*[@value='login']").click()

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
    #pattern = r'<*"0" dy="0.32em">(.*?)<'
    pattern = r'<*"0" dy="0.32em">(.*?)<\/tspan><\/text>'
    #pattern2 = r'<*"0" dy="1.4200000000000002em">(.*?)<'
    tspan_elements = re.findall(pattern, pageData)
    print(tspan_elements)

    for tspan_element in tspan_elements:
        order, name = tspan_element.split(". ")
        name = name.replace('</tspan><tspan x=\"-10\" y=\"0\" dy=\"1.4200000000000002em\">', ' ')
        data.append({
            'name': name,
            'order': order
        })

    closeButton = driver.find_element(By.XPATH, "//a[@class='close']")
    closeButton.click()


driver.close()

import json

output_file = "data.json" 
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False)