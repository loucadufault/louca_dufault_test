from Token import Token
from test_data import *
import re

class Version:
    """
        4.1.0 > 4.1
        1.2b < 1.2
        1.3b > 1.2
        1.31b > 1.319
        1.2b == 1.2B
        1.2a < 1.2b
    """
    # class variables
    delimiter = '.' # the delimiter character that separates sub-versions in a version string, typically the period ('.') char. Can be changed to any other non-word character ([^\w]).
    assert len(delimiter) == 1 and re.match(r"[^\w]", delimiter) # ensure delimitor is set to a single non-word character

    def __init__(self, version):
        p = re.compile(r"^[0-9a-zA-Z]+(?:[{}][0-9a-zA-Z]+)*$".format(self.delimiter)) # one or more (+) alphanumeric chars, followed by zero or more (*) non-capturing (?:...) occurences of a one or more (+) alphanumeric chars preceded by a single delimiter char
        if (p.match(version) is None):
            raise ValueError("Version string supplied must be composed only of sub-versions delimited by '{0}', where the sub-versions contain only alphanumeric characters, and must not start with , end with, or have repeated occurences of the delimiter '{0}'.".format(self.delimiter))
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

    def compare(self, version):
        """Version objects are compared in 4 steps:
        1. the number of tokens of the Version object with the least amount of tokens is found
        2. 
        3. """

        i = 0
        while (i < min(len(self.tokens), len(version.tokens))):
            comparison = self.tokens[i].compare(version.tokens[i])
            if (comparison): # if the result of the compare is not 0, the tokens were not equal
                return comparison

            i += 1
        
        if (len(self.tokens) > len(version.tokens)):
            return self.tokens[i].compare(Token('\0'))

        elif (len(self.tokens) < len(version.tokens)):
            return Token('\0').compare(version.tokens[i])
        
        elif (len(self.tokens) == len(version.tokens)): # all tokens were equal and the versions have the same number of tokens
            return 0 # the tokens are equal

    def compare_special(self, version, ignore_case: bool, lesser_versions: str = None):
        if (ignore_case): # ignore case
            return compare_tokens((self.lower(), version.lower()))

        if (lesser_versions):
            pass

def main():
    test_cases = [version_string for version_string in valid_versions + invalid_versions] # build pairs of Line objects form concatenation of test_data tuples
    test_oracles = (Version,) * len(valid_versions) + (ValueError,) * len(invalid_versions) # commas necessary
    test_results = {"pass": 0, "fail": 0}

    for i, test_case in enumerate(test_cases):
        oracle = test_oracles[i]
        
        print("\nTest case {}:\nChecking whether '{}' is a valid version string".format(i+1, test_case), end=' ') # spread the two Line objects in the test_case tuple into the positional parameters of format as their str representation
        
        try:
            result = Version(test_case)
        except ValueError as e:
            result = e
        finally:
            if (type(result) == oracle):
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