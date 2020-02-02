class Line:
    """A 1D line along the x-axis that is delimited by a start and an end point, each represented by an integer or float."""
    def __init__(self, start, end):
        self.start = min(start, end) # choose the minimum of the endpoints as the start to support out of order parameters
        self.end = max(start, end) # likewise choose the maximum of the endpoints as the end

    @classmethod
    def from_pair(cls, endpoints):
        """Alternate constructor. Call as
        l = Line.from_pair((1, 6))"""
        return cls(endpoints[0], endpoints[1])

    def __repr__(self):
        """Representation of the Line object as a string mimicking the contructor call."""
        return "Line({}, {})".format(self.start, self.end)

    def __str__(self):
        """String representation of the Line object mimicking the initializer passed to the constructor call."""
        return "({}, {})".format(self.start, self.end)

    def get_endpoints(self):
        """Getter that returns the start and end instance variables of the objects as a tuple."""
        return (self.start, self.end)

    def overlaps(self, line):
        """Method to check if the line is overlapping with the line passed as argument.
        Returns True if the lines are overlapping (even in a single point), returns False otherwise."""
        # since the start and end of the lines are ordered in the constructed so that the lesser endpoint is always the start and the greater value is always the end
        return not (self.start > line.end or self.end < line.start) # lines are not overlapping if and only if the start of one is greater than the end of the other, or the end of one is lesser than the start of the other