class Line:
    """A 1D line along the x-axis that is delimited by a start and an end point. """
    def __init__(self, start, end):
        self.start = min(start, end) # choose the minimum of the endpoints as the start to support out of order parameters
        self.end = max(start, end) # likewise choose the maximum of the endpoints as the end

    @classmethod
    def from_pair(cls, endpoints):
        """Alternate constructor. Call as
        l = Line.from_pair((1, 6))"""
        return cls(endpoints[0], endpoints[1])

    def __repr__(self):
        """Representation of the line object as a string mimicking the contructor call."""
        return "Line({}, {})".format(self.start, self.end)
    
    def __str__(self):
        return self.__repr__()

    def overlaps(self, line):
        """Method to check if the line is overlapping with the line passed as argument.
        Returns True if the lines are overlapping (even in a single point), returns False otherwise."""
        
        return not (self.start > line.end or self.end < line.start)