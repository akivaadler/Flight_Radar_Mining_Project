class Fleet:
    """Builds class that contains information about an airlines fleet of aircraft."""
    def __init__(self, type_list):
        self.type_list = type_list
        self.fleet = {}
        self.fleet = {aircraft_type: [] for aircraft_type in type_list}

    def get_plane_list(self, aircraft_type):
        pass

    def get_aircraft(self, aircraft_type, registration):
        pass

    def set_aircraft(self, aircraft):
        """This function checks if the aircraft type or model is in the fleet, and if not, adds it."""
        if aircraft.aircraft_type not in self.fleet.keys():
            self.fleet[aircraft.aircraft_type] = []
        if aircraft not in self.fleet[aircraft.aircraft_type]:
            self.fleet[aircraft.aircraft_type].append(aircraft)

    def get_number_of_aircraft(self):
        """This functions counts the number of aircraft in a fleet."""
        return sum(list(map(lambda x: len(x), list(self.fleet.values()))))

    def __str__(self):
        return f'Fleet: {str(self.__dict__)}'

    def __repr__(self):
        return f'Fleet: {str(self.__dict__)}'
