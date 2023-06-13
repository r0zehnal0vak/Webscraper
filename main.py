# print("hello world")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
pageurl = "https://apl.unob.cz/StudentskeHodnoceni"
driver.get(pageurl) # source <- (pageurl) # http://intranet.unob.cz

#assert "Python" in driver.title

# zadání autentizačních dat
source = driver.page_source # vždy po spuštění kódu
print(source)

elem = driver.find_element(By.NAME, "q") # <-- breakpoint, pozastavení programu pro zadání údajů 
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source

# Selecting options from dropdown menus
dropdown1 = Select(driver.find_element(By.XPATH, "//select[@name='dropdown1_name']"))
dropdown1.select_by_visible_text("Option 1")

dropdown2 = Select(driver.find_element(By.XPATH, "//select[@name='dropdown2_name']"))
dropdown2.select_by_value("option_value")

# Click the enter button (assuming it has an ID attribute)
enter_button = driver.find_element(By.ID, "enter_button_id")
enter_button.click()

driver.close()

reg = "<text([^<]*)<tspan([^>]*)>([^<]*)" # https://regex101.com/

data = []

# driver.find_element_by_xpath("//select[@name='element_name']/option[text()='option_text']").click() # výběr z dropdown menu