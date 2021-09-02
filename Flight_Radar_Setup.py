from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

from Airline import Airline
from Review import Review
from Aircraft import Aircraft
from Fleet import Fleet
from Airport import Airport
from Route import Route

PATH = os.path.join("C:", os.path.sep, "Program Files (x86)", "chromedriver.exe")
WAIT_TIME = 30


def wait_for_and_get_element(driver, element_type, identifier, wait_time=10):
    """This function has an explicit wait, allowing for elements to load before throwing a NoSuchElementError.
    Then it retrieves the element.
    It's parameters are:    driver - Selenium web element driver
                            element_type - the type of web element to identify with (e.g. id, xpath)
                            identifier - the name of the specific element type (e.g. //*[] or id = a)
                            wait_time - amount of time the WebDriverWait function should wait (default = 10)
                            """
    element = None
    if element_type == 'id':
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.ID, identifier)))
        except Exception as e:
            print(e)
            print(element)
            return
    elif element_type == 'xpath':
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, identifier)))
        except Exception as e:
            print(e)
            print(element)
            return
    return element


def main(driver):
    """Contains the web scraping element of the project. Also consolidates the
    data from the different classes into instances of the class Airline."""
    # Accesses the data table of the website
    airlines_table = driver.find_element_by_id("tbl-datatable")

    # Gets list of all of the td's which have a class name of no translate
    # The following line contains the href link to each airline homepage
    airlines_tds = list(airlines_table.find_elements_by_class_name("notranslate"))

    # The following line gets a list of links where each link is a specific airline's home page
    airlines_links = [td.find_element_by_tag_name("a").get_attribute("href") for td in airlines_tds]

    airline_list = []
    airlines_txt = ''
    for airline_index, airline_link in enumerate(airlines_links):
        # click airline_link
        driver.get(airline_link)

        airline_name = (wait_for_and_get_element(driver, 'xpath', '//*[@id="cnt-data-content"]/header/div/div[1]/div[2]/h1')).text
        airline_code = (wait_for_and_get_element(driver, 'xpath', '//*[@id="cnt-data-content"]/header/div/div[1]/div[1]/h2')).text
        print(f'At airline index: {airline_index} and airline name: {airline_name}')

        # get airline tabs
        nav_element = driver.find_element_by_xpath(f'//*[@id="cnt-data-content"]/header/nav')
        airline_tabs_links = list(map(lambda tab: tab.get_attribute("href"), nav_element.find_elements_by_tag_name("a")))

        # specify the relevant tab links
        review_link = airline_tabs_links[1]
        fleet_link = airline_tabs_links[2]
        routes_link = airline_tabs_links[3]

        # driver at reviews page
        driver.get(review_link)
        review_element_list = driver.find_elements_by_css_selector("div.row.cnt-comment")

        content_list = [review_element.find_element_by_class_name("content").text for review_element in review_element_list]
        rating_list = [review_element.find_element_by_class_name("stars").get_attribute("title") for review_element in review_element_list]

        # make a list of Review objects
        review_list = [Review(content, rating.split()[-1]) for content, rating in zip(content_list, rating_list)]

        # navigate to fleet page
        driver.get(fleet_link)

        aircraft_types = wait_for_and_get_element(driver, 'id', 'list-aircraft')

        time.sleep(10) # to ensure that the element loads
        dt_elements = aircraft_types.find_elements_by_tag_name("dt")
        dt_elements = dt_elements[1:]
        dd_elements = aircraft_types.find_elements_by_tag_name("dd")
        type_list = [dt_element.find_elements_by_tag_name("div")[0].text for dt_element in dt_elements]

        # make a Fleet object
        fleet = Fleet(type_list)

        # Get each aircraft type
        for dd_element, aircraft_type in zip(dd_elements, type_list):
            tbody_element = dd_element.find_element_by_tag_name("tbody")
            tr_elements = tbody_element.find_elements_by_tag_name("tr")

            # Build list of aircraft within this aircraft type
            for tr in tr_elements:
                registration_element = tr.find_elements_by_tag_name('td')[0]
                registration = registration_element.find_element_by_tag_name('a').get_attribute('href').split('/')[-1]
                fleet.set_aircraft(Aircraft(aircraft_type, registration))

        aircraft_count = fleet.get_number_of_aircraft()

        # navigate to routes page
        driver.get(routes_link)

        time.sleep(5)
        html_routes_list = driver.execute_script('return arrRoutes')
        routes_list = []
        for route in html_routes_list:
            a1_dict = route['airport1']
            a2_dict = route['airport2']
            airport1 = Airport(a1_dict['name'], a1_dict['country'], a1_dict['iata'],
                               a1_dict['icao'], a1_dict['lat'], a1_dict['lon'])
            airport2 = Airport(a2_dict['name'], a2_dict['country'], a2_dict['iata'],
                               a2_dict['icao'], a2_dict['lat'], a2_dict['lon'])
            routes_list.append(Route(airport1, airport2))

        airline = Airline(airline_name, airline_code, aircraft_count, routes_list, fleet, review_list)
        airline_list.append(airline)
        airlines_txt += f'@\n{airline}'
        f = open('airlines.txt2', 'a+')
        f.write(f'@\n{airline}')
        f.close()
    print(airline_list)

    f = open('airlines.txt', 'w+')
    f.write(airlines_txt)
    f.close()


if __name__ == '__main__':
    chrome_driver = webdriver.Chrome(PATH)
    chrome_driver.implicitly_wait(WAIT_TIME)
    chrome_driver.get("https://www.flightradar24.com/data/airlines")
    try:
        main(chrome_driver)
    finally:
        chrome_driver.quit()

