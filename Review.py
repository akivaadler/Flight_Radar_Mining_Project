class Review:
    """Builds class that contains the top ten reviews of airlines by flightradar
    users. Includes the review content, the rating, the reviewer name, and review date"""
    def __init__(self, content, rating):
        self.rating = rating
        self.content = content



    def __str__(self):
        return f'Review: {str(self.__dict__)}'

    def __repr__(self):
        return f'Review: {str(self.__dict__)}'

