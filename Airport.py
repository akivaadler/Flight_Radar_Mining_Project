class Airport:
    """Builds class that contains information about the different airports that each
    airlines flies into. iata and icao are two different international airport codes, and
    lat and long are the gps coordinates of the airport"""
    def __init__(self, name, country, iata, icao, lat, lon):
        self.name = name
        self.country = country
        self.iata = iata
        self.icao = icao
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return f'Airport: {str(self.__dict__)}'

    def __repr__(self):
        return f'Airport: {str(self.__dict__)}'


