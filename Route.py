class Route:
    """Builds class that contains information about the different airports that each
    airlines flies into. iata and icao are two different international airport codes, and
    lat and long are the gps coordinates of the airport"""

    def __init__(self, airport_1, airport_2):
        self.airport_1 = airport_1
        self.airport_2 = airport_2

    def __str__(self):
        return f'Route: Airport 1: {self.airport_1.name} Airport 2: {self.airport_2.name}'

    def __repr__(self):
        return f'Route: Airport 1: {self.airport_1.name} Airport 2: {self.airport_2.name}'

    def get_distance(self):
        pass
