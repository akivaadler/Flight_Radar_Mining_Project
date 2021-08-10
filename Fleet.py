class Fleet:
    def __init__(self, type_list):
        self.type_list = type_list
        self.fleet = {}
        self.fleet = {aircraft_type: [] for aircraft_type in type_list}

    def get_plane_list(self, aircraft_type):
        pass

    def get_aircraft(self, aircraft_type, registration):
        pass

    def __str__(self):
        return f'Fleet: {str(self.__dict__)}'
