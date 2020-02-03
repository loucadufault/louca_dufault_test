from test_data import *
from Line import Line
import re

def line_overlap(line1_endpoints : list, line2_endpoints : list):
    """Public function to return if two lines supplied as two pairs of enpoints overlap.
    Accepts two lines each as a pair (tuple or list with two items) of integers.
    Returns a boolean value representing whether they overlap."""
    return Line.from_pair(line1_endpoints).overlaps(Line.from_pair(line2_endpoints)) # create anonymous objects
    
def line_overlap_from_string(line1_endpoints_as_string : str, line2_endpoints_as_string : str):
    """Public function to return if two lines supplied as two pairs of enpoints overlap.
    Accepts two lines each as a string containing exactly two decimal values (integer or float) delimited by any non-decimal (excluding periods) character(s).
    Returns a boolean value representing whether they overlap."""
    line1_endpoints = re.findall(r"(?:-?\d+(?:\.\d+)?)", line1_endpoints_as_string)
    line2_endpoints = re.findall(r"(?:-?\d+(?:\.\d+)?)", line2_endpoints_as_string)
    if (len(line1_endpoints) == 2 and len(line2_endpoints) == 2):
        return line_overlap(line1_endpoints, line2_endpoints)
    else:
        raise ValueError("Each line endpoints argument supplied must contain exactly two decimal values (integer or float) delimited by any non-decimal (not a digit or period) character(s).")

def line_overlap_validator(lines, oracle: bool):
    """Validates that the two lines supplied as a pair of Line objects yield the same boolean when checked if they overlap each other as the oracle.
    Throws AssertionError if one line overlaps the other but not vice-versa, and/or if the overlap status of the lines differs from the oracle."""
    assert lines[0].overlaps(lines[1]) == lines[1].overlaps(lines[0]) # check if first Line object overlaps second Line object, and vice-versa
    
    assert lines[0].overlaps(lines[1]) == oracle # check if whether the first Line object overlapping the second Line object is the same as the oracle
    
    # validate public functions
    assert line_overlap(lines[0].get_endpoints(), lines[1].get_endpoints()) == oracle # validate public function
    assert line_overlap_from_string(str(lines[0].get_endpoints()), str(lines[1].get_endpoints())) == oracle # validate wrapper public function
    
def main():
    test_cases = [(Line.from_pair(endpoints[0]), Line.from_pair(endpoints[1])) for endpoints in overlapping + overlapping_edge + not_overlapping_edge + not_overlapping] # build pairs of Line objects form concatenation of test_data tuples
    test_oracles = (True,) * (len(overlapping) + len(overlapping_edge)) + (False,) * (len(not_overlapping_edge) + len(not_overlapping)) # commas necessary
    test_results = {"pass": 0, "fail": 0}

    for i, test_case in enumerate(test_cases):
        oracle = test_oracles[i]
        
        print("\nTest case {}:\nChecking whether {} overlaps {}".format(i+1, *test_case), end=' ') # spread the two Line objects in the test_case tuple into the positional parameters of format as their str representation
        
        try:
            line_overlap_validator(test_case, oracle)
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