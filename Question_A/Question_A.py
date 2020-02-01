from test_data import *

class Line:
    """A 1D line along the x-axis that is delimited by a start and an end point. """
    def __init__(self, start, end):
        self.start = min(start, end) # choose the minimum of the end points as start point to support out of order parameters
        self.end = max(start, end) # likewise choose the maximum

    def __repr__(self):
        """Representation of the line object as a string mimicking the contructor call."""
        return "Line({}, {})".format(self.start, self.end)
    
    def __str__(self):
        return self.__repr__()

    def overlaps(self, line):
        """Method to check if the line is overlapping with the line passed as argument.
        Returns True if the lines are overlapping (even in a single point), returns False otherwise."""
        
        return not (self.start > line.end or self.end < line.start)

def overlap(line1_endpoints, line2_endpoints):
    """Public function to return if two lines supplied as two tuple of enpoints overlap."""
    
    return Line(*line1_endpoints).overlaps(Line(*line2_endpoints)) # create anonymous objects
    
def overlap_validator(lines: tuple, oracle: bool):
    assert lines[0].overlaps(lines[1]) == lines[1].overlaps(lines[0])
    assert lines[0].overlaps(lines[1]) == oracle

def main():
    test_cases = overlapping + overlapping_edge + not_overlapping_edge + not_overlapping
    test_oracles = (True,) * (len(overlapping) + len(overlapping_edge)) + (False,) * (len(not_overlapping_edge) + len(not_overlapping)) # commas necessary
    test_results = {"pass": 0, "fail": 0}

    for i, test_case in enumerate(test_cases):
        oracle = test_oracles[i]
        
        print("\nTest case {}:\nDoes {} overlap {}?".format(i, *test_case), end=' ')
        try:
            overlap_validator(test_case, oracle)
            print("passed", end=' ')
            test_results["pass"] += 1
        except AssertionError:
            print("failed", end=' ')
            test_results["fail"] += 1

        print("(expected {})".format(oracle))

    assert test_results["pass"] + test_results["fail"] == len(test_cases)
    print("\nTest results:\n{} completed, {} failed".format(len(test_cases), test_results["fail"]))

if __name__ == '__main__':
    main()
