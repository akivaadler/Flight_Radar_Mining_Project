class Aircraft:
    """Builds class that contains the aircraft_type and registration number of individual aircraft in an
    airlines fleet"""
    def __init__(self, aircraft_type, registration):
        self.registration = registration
        self.aircraft_type = aircraft_type

    def __str__(self):
        return f'Aircraft: {str(self.__dict__)}'

    def __eq__(self, other_aircraft):
        """Aircraft is equal to another aircraft when the registration and aircraft type are equal."""
        return (self.registration == other_aircraft.registration) and \
               (self.aircraft_type == other_aircraft.aircraft_type)

    def __repr__(self):
        return f'Aircraft: {str(self.__dict__)}'