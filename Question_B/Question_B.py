from test_data import greater, greater_edge, equal, equal_edge, lesser, lesser_edge
from Version import Version

def version_compare(version_string1 : str, version_string2 : str):
    """Public library function to return if a version string greater than, equal, or less than the other.
    Accepts 2 version strings as input arguments.
    Returns an integer > 0 if the first version string was greater than the other, an integer < 0 if the first version string was lesser than the other, and 0 if the version string parameters were equal."""
    return Version(version_string1).compare_with(Version(version_string2)) # create anonymous objects

def greatest_version(version_string1, version_string2):
    """Public library function to return if a version string greater than, equal, or less than the other.
    Accepts accepts 2 version string as inputarguments.
    Returns the version string that is greatest (returns the first version string if equal).
    """
    comparison = version_compare(version_string1, version_string2)
    if (comparison > 0):
        return version_string1
    elif (comparison < 0):
        return version_string2
    else:
        return version_string1

def same_sign(a, b):
    if (abs(a + b) == abs(a) + abs(b)):
        return True
    elif (a == 0 and b == 0):
         return True
    return False

def version_compare_validator(versions, oracle: bool):
    """Validates that the two versions supplied as a pair of Version objects yield an integer of the same sign as the oracle, or the same value as the oracle if it is 0, when the first Version object is compared to the second
    Throws AssertionError if the comparison of the first Version object with the second Version objects yields an integer result that differs in sign from the oracle, or in value if the oracle is 0."""
    assert same_sign(versions[0].compare_with(versions[1]), oracle)
    
    # validate public functions
    assert same_sign(version_compare(str(versions[0]), str(versions[1])), oracle)
    assert greatest_version(str(versions[0]), str(versions[1])) == [str(versions[1]), str(versions[0]), str(versions[0])][oracle+1]

def test():
    test_cases = [(Version(version_strings[0]), Version(version_strings[1])) for version_strings in greater + greater_edge + equal + equal_edge + lesser_edge + lesser] # build pairs of Version objects from tuples in the concatenation of test_data arrays
    test_oracles = (1,) * (len(greater) + len(greater_edge)) + (0,) * (len(equal) + len(equal_edge)) + (-1,) * (len(lesser_edge) + len(lesser)) # commas necessary
    test_results = {"pass": 0, "fail": 0}

    for i, test_case in enumerate(test_cases):
        oracle = test_oracles[i]
        
        print("\nTest case {}:\nComparing version string '{}' with version string '{}'".format(i+1, *test_case), end=' ') # spread the two Version objects in the test_case tuple into the positional parameters of format as their str representation
        
        try:
            version_compare_validator(test_case, oracle)
            print("passed", end=' ')
            test_results["pass"] += 1
        except AssertionError:
            print("failed", end=' ')
            test_results["fail"] += 1

        print("(expected {}).".format({"1": "> 1", "0": "0", "-1": "< 1"}[str(oracle)]))

    assert test_results["pass"] + test_results["fail"] == len(test_cases) # ensure all tests have been completed
    print("\nTest results:\n{} completed, {} failed".format(len(test_cases), test_results["fail"])) # display results

def main():
    test()

if __name__ == '__main__': # if run standalone
    main() # unit test this module
