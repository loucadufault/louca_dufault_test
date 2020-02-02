from Token import Token
from test_data import *
import re

class Version:
    """
        4.1.0 > 4.1
        1.2b < 1.2
        1.3b > 1.2
        1.31b > 1.31a
        1.2b == 1.2B
        1.2a < 1.2b
    """
    # class variables
    delimiter = '.' # the delimiter character that separates sub-versions in a version string, typically the period ('.') char. Can be changed to any other non-word character ([^\w]).
    assert len(delimiter) == 1 and re.match(r"[^\w]", delimiter) # ensure delimitor is set to a single non-word character

    def __init__(self, version):
        version = version.lower()
        p = re.compile(r"[a-zA-Z]+$") # one or more letters at the end of the version string
        try:
            self.suffix = p.search(version).group() # set the instance variable suffix to that sequence of letters at the end of the string
            version = p.sub('', version) # remove the alphabetical suffix from the version string
        except AttributeError: # re.search() did not match, there is no alphabetical suffix
            self.suffix = '@' # set the suffix to the ascii code preceding the first lowercase alphabetical character ('a'), for comparing suffixes later on
        
        # version string must match one or more (+) digits, followed by zero or more (*) non-capturing (?:...) occurences of a one or more (+) digits preceded by a single delimiter char
        if (re.match(r"^\d+(?:[{}]\d+)*$".format(self.delimiter), version) is None):
            raise ValueError("Version string supplied must be composed only of digits delimited by '{0}', and must not start with, end with, or have repeated occurences of the delimiter '{0}'.".format(self.delimiter))
        self.tokens = self.tokenize(version)

    def __repr__(self):
        """Representation of the Version object as a string mimicking the contructor call."""
        return "Version({})".format(str(self))

    def __str__(self):
        """String representation of the Version object mimicking the initializer passed to the constructor call (without the delimiter)."""
        return self.untokenize()

    def tokenize(self, version):
        tokens = []
        for sub_string in version.split(self.delimiter):
            tokens.append(Token(sub_string))
        return tuple(tokens) # token array is immutable

    def untokenize(self):
        return (self.delimiter).join([str(token) for token in self.tokens])

    def compare_suffix(self, version):
        i = 0
        while ((i < min(len(self.suffix), len(version.suffix)) - 1) and (self.suffix[i] == version.suffix[i])):
            i += 1
        return self.suffix[i] == version.suffix[i]

    def compare(self, version):
        """Version objects are compared in 4 steps:
        1. Iterate over the tokens of both Version objects until reaching the last token of the shorter Version object (fewer tokens) 
        2. For each Token object, compare the Token object of the self Version to the corresponding token of the parameter Version
        3. If they are equal, continue to the next token, otherwise return the integer result of the comparison
        4. If the end of the shorter list of tokens is reached, return the integer value of the next token of the Version object with more tokens, positive if it is the self object and negative if it is the parameter object
        5. If both Version objects had the same number of tokens, compare the suffixes of both Token object and return the integer result of the comparison
        6. If both suffixes are equal return 0 since bothe Version objects are identical
        3. """

        i = 0
        while (i < min(len(self.tokens), len(version.tokens))):
            comparison = self.tokens[i].compare(version.tokens[i])
            if (comparison): # if the result of the compare is not 0, the tokens were not equal
                return comparison

            i += 1
        
        if (len(self.tokens) > len(version.tokens)):
            return int(self.tokens[i])

        elif (len(self.tokens) < len(version.tokens)):
            return -int(version.tokens[i])
        
        elif (len(self.tokens) == len(version.tokens)): # all tokens were equal and the versions have the same number of tokens
            comparison = self.compare_suffix(version)
            if (comparison):
                return comparison
            else:
                return 0 # the tokens are equal

def main():
    test_cases = [version_string for version_string in valid_versions + invalid_versions] # build list of version strings from test_data
    test_oracles = (Version,) * len(valid_versions) + (ValueError,) * len(invalid_versions) # commas necessary
    test_results = {"pass": 0, "fail": 0}

    for i, test_case in enumerate(test_cases):
        oracle = test_oracles[i]
        
        print("\nTest case {}:\nChecking whether '{}' is a valid version string".format(i+1, test_case), end=' ') # spread the two Line objects in the test_case tuple into the positional parameters of format as their str representation
        
        try:
            result = Version(test_case)
        except ValueError as e: # necessary to transfer caught error to result since scope of error is 'except' block
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