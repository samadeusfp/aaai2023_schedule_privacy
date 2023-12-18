# jobs only have 2 relevant features for the twct: processing time and weight.
class Job:
    def __init__(self, id: int, processing_time: int, weight: int):
        self.id = id
        self.processing_time = processing_time
        self.weight = weight

    def __eq__(self, other):
        return (isinstance(other, Job)
                and self.id == other.id
                and self.weight == other.weight
                and self.processing_time == other.processing_time)

    def tuple(self):
        return (self.id, self.processing_time, self.weight)

    def __hash__(self):
        return hash(self.tuple())

    def __str__(self):
        return f"({self.id}, {self.processing_time}, {self.weight})"
