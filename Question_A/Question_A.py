from test_data import *
from Line import Line

def overlap(line1_endpoints, line2_endpoints):
    """Public function to return if two lines supplied as two pairs of enpoints overlap."""
    return Line.from_pair(line1_endpoints).overlaps(Line.from_pair(line2_endpoints)) # create anonymous objects
    
def overlap_validator(lines, oracle: bool):
    """Validates that the two lines supplied as a pair of Line objects yield the same boolean when checked if they overlap each other as the oracle.
    Throws AssertionError if one line overlaps the other but not vice-versa, and if the overlap status of the lines differs from the oracle."""
    assert lines[0].overlaps(lines[1]) == lines[1].overlaps(lines[0]) # check if first Line object overlaps second Line object, and vice-versa
    assert lines[0].overlaps(lines[1]) == oracle # check if whether the first Line object overlapping the second Line object is the same as the oracle
    assert overlap(lines[0].get_endpoints(), lines[1].get_endpoints()) == oracle # validate public function

def main():
    test_cases = [(Line.from_pair(endpoints[0]), Line.from_pair(endpoints[1])) for endpoints in overlapping + overlapping_edge + not_overlapping_edge + not_overlapping] # build pairs of Line objects form concatenation of test_data tuples
    test_oracles = (True,) * (len(overlapping) + len(overlapping_edge)) + (False,) * (len(not_overlapping_edge) + len(not_overlapping)) # commas necessary
    test_results = {"pass": 0, "fail": 0}

    for i, test_case in enumerate(test_cases):
        oracle = test_oracles[i]
        
        print("\nTest case {}:\nChecking whether {} overlaps {}".format(i+1, *test_case), end=' ') # spread the two Line objects in the test_case tuple into the positional parameters of format as their str representation
        
        try:
            overlap_validator(test_case, oracle)
            print("passed", end=' ')
            test_results["pass"] += 1
        except AssertionError:
            print("failed", end=' ')
            test_results["fail"] += 1

        print("(expected {}).".format(oracle))

    assert test_results["pass"] + test_results["fail"] == len(test_cases) # ensure all tests have been completed
    print("\nTest results:\n{} completed, {} failed".format(len(test_cases), test_results["fail"])) # display results

if __name__ == '__main__':
    main()