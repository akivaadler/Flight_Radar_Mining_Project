class Review:
    def __init__(self, name, date, stars, text):
        self.name = name
        self.date = date
        self.stars = stars
        self.text = text

    def __str__(self):
        return f'Review: {str(self.__dict__)}'
