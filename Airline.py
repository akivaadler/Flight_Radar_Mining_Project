class Airline:
    def __init__(self, name, code, num_aircraft, routes, fleet, reviews):
        self.name = name
        self.code = code
        self.num_aircraft = num_aircraft
        self.routes = routes
        self.fleet = fleet
        self.reviews = reviews

    def __str__(self):
        return f'Airline: {str(self.__dict__)}'
