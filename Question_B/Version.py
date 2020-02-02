from Token import Token
from test_data import *
import re

class Version:
    """
        4.1.0 > 4.1
        1.2b < 1.2
        1.3b > 1.2
        1.2b == 1.2B
        1.2a < 1.2b
    """
    # class variables
    delimiter = '.' # the delimiter character that separates sub-versions in a version string, typically the period ('.') char. Can be changed to any other non-word character ([^\w]).
    assert len(delimiter) == 1 and re.match(r"[^\w]", delimiter) # ensure delimitor is set to a single non-word character

    def __init__(self, version):
        p = re.compile(r"^\w+(?:[{}]\w+)*$".format(self.delimiter)) # one or more (+) word chars, followed by zero or more (*) non-capturing (?:...) occurences of a one or more (+) word chars preceded by a single delimiter char
        # will find 1, 1.2.9, 1.2_45.3b, 0.11a
        # will not find 1.5., .081.4,  3.4..56
        if (p.match(version) is None):
            raise ValueError("Version string supplied must be composed only of sub-versions delimited by '{0}', where the sub-versions contain only alphanumeric or underscore ('_') characters, and must not startwith , end with, or have repeated occurences of the delimiter '{0}'.".format(self.delimiter))
        self.tokens = self.tokenize(version)

    def __repr__(self):
        """Representation of the Version object as a string mimicking the contructor call."""
        return "Version({})".format(self.untokenize())

    def __str__(self):
        """String representation of the Version object mimicking the initializer passed to the constructor call (without the delimiter)."""
        return self.untokenize()

    def tokenize(self, version):
        tokens = []
        for sub_string in version.split(self.delimiter):
            tokens.append(Token(sub_string))
        return tuple(tokens)

    def untokenize(self):
        return (self.delimiter).join([str(token) for token in self.tokens])

    def lower(self):
        return [token.lower() for token in self.tokens]
        # lower_tokens = []
        # for token in self.tokens:
        #     lower_tokens.append(token.lower())
        
        # return lower_tokens

    def compare(self, version):
        """Version objects are compared in 4 steps:
        1. the version instance variable of each object is tokenized on the period "." character into a list of substrings
        2. find the length of the shortest list of substrings and store it in n
        3. """

        n = min(len(self.tokens), len(version.tokens))
        i = 0
        while (i < n):
            if (i == len(self.tokens) or i == len(version.tokens)):
                break

            comparison = self.tokens[i].compare(version.tokens[i])
            if (comparison): # if the result of the compare is not 0, the tokens were not equal
                return comparison

        if (len(version_tokens[0]) == len(version_tokens[1])): # all tokens were equal and the versions have the same number of tokens
            return 0 # the tokens are equal
        
        #if Token('\0').compare()

    def compare_special(self, version, ignore_case: bool, lesser_versions: str = None):
        if (ignore_case): # ignore case
            return compare_tokens((self.lower(), version.lower()))

        if (lesser_versions):
            pass

def main():
    test_cases = [version_string for version_string in valid_versions + invalid_versions] # build pairs of Line objects form concatenation of test_data tuples
    test_oracles = (type(None),) * len(valid_versions) + (ValueError,) * len(invalid_versions) # commas necessary
    test_results = {"pass": 0, "fail": 0}

    for i, test_case in enumerate(test_cases):
        oracle = test_oracles[i]
        
        print("\nTest case {}:\nChecking whether '{}' is a valid version string".format(i+1, test_case), end=' ') # spread the two Line objects in the test_case tuple into the positional parameters of format as their str representation
        
        ge = None
        try:
            Version(test_case)
        except ValueError as le:
            ge = le
        finally:
            if (type(ge) == oracle):
                print("passed", end=' ')
                test_results["pass"] += 1
            else:
                print("failed", end=' ')
                test_results["fail"] += 1

        print("(expected {}).".format(str(oracle)))

    assert test_results["pass"] + test_results["fail"] == len(test_cases) # ensure all tests have been completed
    print("\nTest results:\n{} completed, {} failed".format(len(test_cases), test_results["fail"])) # display results

if __name__ == '__main__':
    main()