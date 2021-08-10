class Airport:
    def __init__(self, name, country, iata, icao, lat, lon):
        self.name = name
        self.country = country
        self.iata = iata
        self.icao = icao
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return f'Airport: {str(self.__dict__)}'


