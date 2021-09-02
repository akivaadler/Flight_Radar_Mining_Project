# Flight_Radar_Mining_Project

**Authors**

[Akiva Adler](https://github.com/akivaadler) & [Alon Gabbay](https://github.com/AlonGabbay)


**Overview**

The airline idustry is a complex system. Airlines, aicraft, airports, and many other elements are required to work together in order to make the whole system work. [FlightRadar](https://www.flightradar24.com/31.78,35.23/3) is a website that not only presents the web of global flights in real time, but it also stores lots of data about different aircraft and airlines. We wanted to scrape this data from the website in order to use the data downstream. 

**What We Did**

Our approach was to build individual class for each set of data, and then consolidate them into instances of the class Airline, which contains the name of the airline, the airline code, the number of aircraft in the airlines' fleet, details about the fleet, the different routes the airlines run, and reviews that users posted about the airline. We printed each Airline instance into a text file. 

**Some Things We Learned**

1. To work with Selenium.
2. How to work on code as a team.
3. The power of googling.
4. How to maneuver Git and Github.
5. Persistence and hard work pay off.

**How To Use This Repo**

1. Clone the repo
2. Open as a python project
3. Install the required packages using the pip install - r requirements.txt command in the terminal
4. Run the Flight_Radar_Setup.py file
5. At the end of the run, 'airline.txt' will appear in your local files and will include the output

    **The output will have the following format:**

      a. The airline name

      b. The airline code

      c. The number of aircraft in the fleet of the airline

      d. A list of routes that the airline runs

      e. A dictionary that includes the aircraft types in the fleet, as well as information about each aircraft in each aircraft type

      f. A list of reviews (rating and content) that users have posted on the website
  
**Thanks For Reading!**
