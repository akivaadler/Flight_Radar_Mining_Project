from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.flightradar24.com/data/airlines")
print(driver.title)


airlines_table = driver.find_element_by_id("tbl-datatable")
# search.send_keys("test")
# search.send_keys(Keys.RETURN)
airlines = airlines_table.find_elements_by_tag_name("tr")
#TODO Need condition in loop - If tr has class, continue (in order to filter out the header rows)

print(airlines)
print(airlines[2])
# try:
#     main = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "main"))
#     )
#     airlines_table = main.find_element_by_id("tbl-datatable")
#     print(airlines_table)
#     #for airline in airlines_table:
#         #header = article.find_element_by_class_name("entry-meta")
#         #print(header.text)
# except:
#     driver.quit()





driver.quit()