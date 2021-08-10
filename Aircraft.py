class Aircraft:
    def __init__(self, model, registration):
        self.registration = registration
        self.model = model

    def __str__(self):
        return f'Aircraft: {str(self.__dict__)}'
