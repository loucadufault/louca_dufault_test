from test_data import *

class Line:
    def __init__(self, start, end):
        self.start = min(start, end)
        self.end = max(start, end)

    def __repr__(self):
        return "Line({}, {})".format(self.start, self.end)
    
    def __str__(self):
        return self.__repr__()
        #print("Line from {} to {} on the x-axis.".format(self.start, self.end))

    def overlaps(self, line):
        return not (self.start > line.end or self.end < line.start)

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