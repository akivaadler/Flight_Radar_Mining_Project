from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

PATH = os.path.join("C:", os.path.sep, "Program Files (x86)", "chromedriver.exe")



"""
Airlines
Fleet - Done
Aircraft - Done
Airport - Done
Review - Done
Routes
Serial number can be an index
Row 51 is the dictionary that includes all of the airports of an airline
"""


def main(driver):
    # Accesses the data table of the website
    airlines_table = driver.find_element_by_id("tbl-datatable")

    # Gets list of all of the td's which have a class name of no translate
    # The following line contains the href link to each airline homepage
    airlines_tds = list(airlines_table.find_elements_by_class_name("notranslate"))

    # The following line gets a list of links where each link is a specific airline's home page
    airlines_links = [td.find_element_by_tag_name("a").get_attribute("href") for td in airlines_tds]

    airline_list = []
    print(airlines_links[0])

    for link in airlines_links[:1]:
        # click link
        driver.get(link)
        # click on review
        # nav = driver.find_element_by_class_name("btn-group btn-block")
        # airline_review = nav.find_element_by_link_text("  Reviews ").click()

        # make a Review object
        # make a Fleet object
        # for loop for each aircraft
        # enter data into airline object
        # add airline object to airline list
    driver.quit()



if __name__ == '__main__':
    chrome_driver = webdriver.Chrome(PATH)
    chrome_driver.get("https://www.flightradar24.com/data/airlines")
    main(chrome_driver)
    # try:
    #     main_2 = WebDriverWait(chrome_driver, 10).until(
    #         EC.presence_of_element_located((By.ID, "main"))
    #     )
    #     chrome_driver.get("https://www.flightradar24.com/data/airlines")
    #     main(chrome_driver)
    # except Exception as e:
    #     chrome_driver.quit()
    #     print(e)
