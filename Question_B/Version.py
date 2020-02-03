from Token import Token
from test_data import *
import re

class Version:
    """
        4.1.0 == 4.1
        1.2b < 1.2
        1.3b > 1.2
        1.31b > 1.31a
        1.3b < 1.3.4.5
        1.2b == 1.2B
        1.2a < 1.2b
    """
    # class variables
    delimiter = '.' # the delimiter character that separates sub-versions in a version string, typically the period ('.') char. Can be changed to any other non-word character ([^\w]).
    assert len(delimiter) == 1 and re.match(r"[^0-9a-zA-Z]", delimiter) # ensure delimitor is set to a single non-alphanumeric character

    def __init__(self, version):
        version = version.lower()
        p = re.compile(r"[a-zA-Z]+$") # one or more letters at the end of the version string
        try:
            self.suffix = p.search(version).group() # set the instance variable suffix to that sequence of letters at the end of the string
            version = p.sub('', version) # remove the alphabetical suffix from the version string
        except AttributeError: # re.search() did not match, there is no alphabetical suffix
            self.suffix = '' # set the suffix to an empty string to indicate it is absent from the version string that the object represents
        
        # version string must match one or more (+) digits, followed by zero or more (*) non-capturing (?:...) occurences of a one or more (+) digits preceded by a single delimiter char
        if (re.match(r"^\d+(?:[{}]\d+)*$".format(self.delimiter), version) is None):
            raise ValueError("Version string supplied must be composed only of digits delimited by '{0}', and must not start with, end with, or have repeated occurences of the delimiter '{0}'.".format(self.delimiter))
        self.tokens = self.tokenize(version)

    def __repr__(self):
        """Representation of the Version object as a string mimicking the contructor call."""
        return "Version({})".format(str(self))

    def __str__(self):
        """String representation of the Version object mimicking the version string initializer passed to the constructor call."""
        return self.untokenize() + self.suffix

    def tokenize(self, version):
        tokens = []
        for sub_string in version.split(self.delimiter):
            tokens.append(Token(sub_string))
        return tuple(tokens) # token array is immutable

    def untokenize(self):
        return (self.delimiter).join([str(token) for token in self.tokens])

    def compare_suffix_with(self, version):
        """
        """
         # if neither Version objects have a suffix
        if (not self.suffix and not version.suffix):
            return 0
        # if one Version object has a suffix but not the other
        elif (not version.suffix): # if the self object has a suffix but the version object does not have a suffix, the latter is considered greater
            return -(ord(self.suffix[0]) - ord('`')) # the opposite of its ASCII code is returned, since a negative return means the self object (object upon which the method call was made) is lesser
        elif (not self.suffix): # if the self object does not have a suffix but the version object has a suffix, the former is considered greater
            return (ord(version.suffix[0]) - ord('`')) # # its ASCII code is returned, since a positive return means the self object (object upon which the method call was made) is greater
        # where '`' is the character whose ascii code preceeds the first lowercase alphabetical character ('a'), and where ord() is a buitlin function that yields the ASCII code of a character
        
        # if both Version objects have a suffix
        i = 0
        while ((i < min(len(self.suffix), len(version.suffix)))): # iterate through the suffixes until reaching the end of the shortest suffix
            if (self.suffix[i] != version.suffix[i]):
                return ord(self.suffix[i]) - ord(version.suffix[i])
            i += 1

        # reached the end of the shortest suffix

        if (len(self.suffix) == len(version.suffix)): # if both suffixes had the same length
            return 0

        try:
            return ord(self.suffix[i]) - ord('`')
        except IndexError:
            return -(ord(version.suffix[i]) - ord('`'))

    def compare_with(self, version):
        """
        Algorithm for comparing version objects:
        1. Iterate over the tokens of both Version objects until reaching the last token of the shorter Version object (fewer tokens) 
        2. For each Token object, compare the Token object of the self Version to the corresponding token of the parameter Version
        3. If the Token objects are equal (equal integer values), continue to the next token, otherwise return the integer result of the comparison
        4. If the end of the shorter list of tokens is reached, return the integer value of the next token of the Version object with more tokens, positive if it is the self object and negative if it is the parameter object
        5. If both Version objects had the same number of tokens, compare the suffixes of both Token object and return the integer result of the comparison
        6. If both suffixes are equal return 0 since bothe Version objects are identical
        """

        i = 0
        while (i < min(len(self.tokens), len(version.tokens))): # iterate over the tokens of both Version objects until reaching the last token of the shorter Version object (fewer tokens) 
            comparison = self.tokens[i].compare(version.tokens[i]) # compare the Token object of the self Version to the corresponding token of the parameter Version
            if (comparison): # if the result of the compare is not 0, the tokens were not equal
                return comparison # return the integer result of the comparison

            i += 1 # otherwise the Token objects were equal (equal integer values), continue to the next token by incrementing counter
        
        # end of the shorter list of tokens is reached
        # , return the integer value of the next token of the Version object with more tokens, positive if it is the self object and negative if it is the parameter object
        if (len(self.tokens) > len(version.tokens)): # if the self Version object has more tokens
            return int(self.tokens[i]) # return the integer value of the next Token object in the self Version object's tokens list
            # may also return 0 if the next token of the self Version object is '0' or '000...', as such versions '1.2.0' and '1.2' are chosen to be identical

        elif (len(self.tokens) < len(version.tokens)): # if the version Version object has more tokens
            return -int(version.tokens[i]) # return the opposite (to show that the self object is lesser than the version object) of the integer value of the next Token object in the version Version object's tokens list
            # may also return 0 if the next token of the version Version object is '0' or '000...', as such versions '1.2' and '1.2.0' are chosen to be identical

        elif (len(self.tokens) == len(version.tokens)): # all tokens were equal and the versions have the same number of tokens
            comparison = self.compare_suffix_with(version) # compare the optional suffixes of both Version objects, if neither Version object represents a version string with a suffix, the comparison yields 0 as expected
            if (comparison): # if the result of the compare is not 0, the suffixes were not equal, or one Version object had a suffix while the other did not
                return comparison # return the integer result of the comparison
            else: # otherwise the suffix strings were equal (same length and identical characters, ignoring case) or neither Version object had a suffix
                return 0 # the Version objects are identical (ignoring case of the suffixes)

def main():
    test_cases = [version_string for version_string in valid_version_strings + invalid_version_strings] # build list of version strings from test_data
    test_oracles = (Version,) * len(valid_version_strings) + (ValueError,) * len(invalid_version_strings) # commas necessary
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

if __name__ == '__main__': # if run standalone
    main() # unit test this module
