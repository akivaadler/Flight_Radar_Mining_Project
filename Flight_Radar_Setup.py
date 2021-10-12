from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time
import argparse

from Airline import Airline
from Review import Review
from Aircraft import Aircraft
from Fleet import Fleet
from Airport import Airport
from Route import Route

from db_connection import *

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

def get_chromedriver():
    chromedriver_autoinstaller.install()
    chrome_driver = webdriver.Chrome()
    chrome_driver.implicitly_wait(WAIT_TIME)
    return chrome_driver


def get_all_airline_links_and_names(driver):
    driver.get("https://www.flightradar24.com/data/airlines")
    time.sleep(1)

    # Accesses the data table of the website
    airlines_table = driver.find_element_by_id("tbl-datatable")

    # Gets list of all of the td's which have a class name of no translate
    # The following line contains the href link to each airline homepage
    airlines_tds = list(airlines_table.find_elements_by_class_name("notranslate"))

    # The following line gets a list of a tags.
    a_tags = [td.find_element_by_tag_name("a") for td in airlines_tds]

    airline_links = [a_tag.get_attribute("href") for a_tag in a_tags]
    airline_names = [a_tag.get_attribute("title") for a_tag in a_tags]

    return airline_links, airline_names

# def get_all_airline_links(driver):
#     a_tags = get_all_airline_a_tags(driver)
#     return [a_tag.get_attribute("href") for a_tag in a_tags],
#
#
# def get_airline_names(driver):
#     a_tags = get_all_airline_a_tags(driver)
#     return [a_tag.get_attribute("title") for a_tag in a_tags]


def get_requested_airline_links(driver, request=(0,2)):
    # airlines_links = get_all_airline_links(driver)
    # airlines_names = get_airline_names(driver)
    airlines_links, airlines_names = get_all_airline_links_and_names(driver)
    requested_airline_links = []
    if isinstance(request, list):
        if all(isinstance(element, int) for element in request):
            # is indexes
            for index in request:
                if not(0 <= index <= len(airlines_links)):
                    raise IndexError(f"The index {index} is out of these 0 - {len(airlines_links) -1} bounds.")
                requested_airline_links.append(airlines_links[index])
        elif all(isinstance(element, str) for element in request):
            for name in request:
                if name not in airlines_names:
                    raise ValueError(f"The airline name {name} is not one of the airline names.")
                requested_airline_links.append(airlines_links[airlines_names.index(name)])

    elif isinstance(request, tuple):
        if len(request) != 2:
            raise ValueError(f'Please enter a range of two numbers')
        elif not isinstance(request[0], int) and not isinstance(request[1], int):
        #elif isinstance(request[0], int) and isinstance(request[1], int):
            raise TypeError(f'Range of numbers must be integers and not {request[0]} or {request[1]}')
        elif request[0] > request[1] or request[0] < 0 or request[1] >= len(airlines_links):
            raise ValueError(f'Please enter an acceptable range between 0 and {len(airlines_links) -1}')
        requested_airline_links = airlines_links[request[0]:request[1]+1]
    else:
        raise TypeError(f'Please use a correct way of requesting airlines.')

    return requested_airline_links

def get_reviews(driver, review_link):

    driver.get(review_link)
    time.sleep(1)
    review_element_list = driver.find_elements_by_css_selector("div.row.cnt-comment")

    content_list = [review_element.find_element_by_class_name("content").text for review_element in review_element_list]
    rating_list = [review_element.find_element_by_class_name("stars").get_attribute("title") for review_element in
                   review_element_list]

    # make a list of Review objects
    review_list = [Review(content, rating.split()[-1]) for content, rating in zip(content_list, rating_list)]

    return review_list

def get_fleet(driver, fleet_link):
    driver.get(fleet_link)

    aircraft_types = wait_for_and_get_element(driver, 'id', 'list-aircraft')

    time.sleep(10)  # to ensure that the element loads
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

    return fleet

def get_routes(driver, routes_link):
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

    return routes_list


def get_airline(driver, airline_link):
    driver.get(airline_link)
    time.sleep(1)

    airline_name = (wait_for_and_get_element(driver, 'xpath', '//*[@id="cnt-data-content"]/header/div/div[1]/div[2]/h1')).text
    airline_code = (wait_for_and_get_element(driver, 'xpath', '//*[@id="cnt-data-content"]/header/div/div[1]/div[1]/h2')).text

    review_link, fleet_link, routes_link = get_airline_tabs(driver, airline_link)

    fleet = get_fleet(driver, fleet_link)
    routes = get_routes(driver, routes_link)
    reviews = get_reviews(driver, review_link)

    return Airline(airline_name, airline_code, routes, fleet, reviews)


def get_airline_tabs(driver, airline_link):
    driver.get(airline_link)
    time.sleep(1)

    airline_name = (wait_for_and_get_element(driver, 'xpath', '//*[@id="cnt-data-content"]/header/div/div[1]/div[2]/h1')).text
    airline_code = (wait_for_and_get_element(driver, 'xpath', '//*[@id="cnt-data-content"]/header/div/div[1]/div[1]/h2')).text
    #print(f'At airline index: {airline_index} and airline name: {airline_name}')

    # get airline tabs
    nav_element = driver.find_element_by_xpath(f'//*[@id="cnt-data-content"]/header/nav')
    airline_tabs_links = list(map(lambda tab: tab.get_attribute("href"), nav_element.find_elements_by_tag_name("a")))


    # specify the relevant tab links
    review_link = airline_tabs_links[1]
    fleet_link = airline_tabs_links[2]
    routes_link = airline_tabs_links[3]

    return review_link, fleet_link, routes_link


def get_airline_info(driver, airline_link, choice):

    if not isinstance(choice, str):
        raise TypeError('Please enter one of the following: "fleet", "route", "review", or "airline"')

    possible_choices = ['fleet', 'route', 'review', 'airline']

    if choice not in possible_choices:
        raise ValueError(f'The choice {choice} is not in the possible choices, which are: {possible_choices}')

    review_link, fleet_link, routes_link = get_airline_tabs(driver, airline_link)

    if 'fleet' == choice:
        return get_fleet(driver, fleet_link)

    if 'route' == choice:
        return get_routes(driver, routes_link)

    if 'review' == choice:
        return get_reviews(driver, review_link)

    if 'airline' == choice:
        return get_airline(driver, airline_link)


def get_args(parser):
    args_dict = vars(parser.parse_args())
    arg_list = []
    for key, value in args_dict.items():
        if key == 'range' and value is not None:
            value = tuple(value)
        if value is not None:
            arg_list.append(value)

    return arg_list


def cli_main():

    possible_choices = ['fleet', 'route', 'review', 'airline']

    parser = argparse.ArgumentParser(description='Scrape some airline data')
    group = parser.add_mutually_exclusive_group(required=True)

    parser.add_argument('choice', metavar='choice', type=str,
                        help='specific info about an airline', choices=possible_choices)
    group.add_argument('-indexes', metavar='index', type=int, nargs='+',
                        help='indexes for which airline')
    group.add_argument('-names', metavar='name', type=str, nargs='+',
                        help='names for which airline')
    group.add_argument('-range', metavar='N', type=int, nargs=2,
                        help='range for which airlines')

    #print('steve', parser.parse_args())
    driver = get_chromedriver()
    result_list = []
    try:
        choice, request = get_args(parser)
        links = get_requested_airline_links(driver, request)
        cur = get_connection()

        for index, link in enumerate(links):
            result_list.append(get_airline_info(driver, link, choice))
            print(result_list[index])

            result_item = get_airline_info(driver, link, choice)
            for result in result_item:
                for index, review in enumerate(result):
                    print(index, review) #add iterators to classes into order to "grab" them individually?

        # TODO add airline_id to the different classes
        # TODO write function/ try & excep that builds an SQL query based on "choice" & "request" in order to determine if already in DB
        # TODO or do try and except for the insert command, and that resolves the need for a function with 12 if's
            #cur.execute('INSERT INTO table_name VALUES (?,?,?,?)', )
        # query_dict = {}
        # execute_and_display(cur, )




    except (ValueError, TypeError, IndexError) as e:
        print(e)
    finally:
        driver.quit()
    #TODO check range as input
    #TODO check list of indexes as input
    #TODO add name of output airline
    #TODO add note if empty list
    #TODO error needs to close the window also






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

    for airline_index, airline_link in enumerate(airlines_links[0:2]):
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

        f = open('airlines.txt', 'a+')
        f.write(f'@\n{airline}')
        f.close()

def my_sum(a):
     return sum(a)


if __name__ == '__main__':
    cli_main()
