class Airline:
    """Builds class that contains information about individual airlines"""
    def __init__(self, name, code, routes, fleet, reviews):
        self.name = name
        self.code = code
        self.num_aircraft = fleet.get_number_of_aircraft()
        self.routes = routes
        self.fleet = fleet
        self.reviews = reviews

    def _get_string(self):
        airline_str = ''
        airline_str += f'Airline Name: {self.name} \n'
        airline_str += f'Airline Code: {self.code} \n'
        airline_str += f'Airline Size of Fleet: {self.num_aircraft} \n'
        airline_str += f'Airline Routes: {self.routes} \n'
        airline_str += f'Airline Fleet: {self.fleet} \n'
        airline_str += f'Airline Reviews: {self.reviews} \n'
        return airline_str

    def __str__(self):
        return self._get_string()

    def __repr__(self):
        return self._get_string()
