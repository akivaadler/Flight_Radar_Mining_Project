class AircraftSchedule:
    """Builds class that contains the schedule of individual planes in an airline. std is
    scheduled time departure, atd is actual time departure, sta is scheduled time arrival"""
    def __init__(self, date, origin, destination, flight_num, flight_time, std, atd, sta, status):
        self.date = date
        self.origin = origin
        self.destination = destination
        self.flight_num = flight_num
        self.flight_time = flight_time
        self.std = std  # Scheduled Time Departure
        self.atd = atd  # Actual Time Departure
        self.sta = sta  # Scheduled Time Arrival
        self.status = status  # Flight status

    def __str__(self):
        return f'Aircraft_Schedule: {str(self.__dict__)}'

    #This is a test
    def test(self):
        self.a = self.date
