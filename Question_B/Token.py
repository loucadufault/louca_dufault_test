class Token:
    def __init__(self, content):
        self.content =  content.lower()
    
    def __repr__(self):
        """Representation of the Token object as a string mimicking the contructor call."""
        return "Token({})".format(self.content)

    def __str__(self):
        """String representation of the Token object mimicking the initializer passed to the constructor call."""
        return self.content
    
    def compare(self, token):
        i = 0
        while (True):
            if (i == len(self.content) or i == len(token.content)):
                break

            comparison = ord(self.content[i]) - ord(token.content)
            if (comparison):
                return comparison

        if (len(self.content) == len(token.content)): # all characteres in token were equal and the tokens have the same length
            return 0 # the tokens are equal
        

    def isalpha(self):
        for char in self.content:
            if (not char.isalpha()):
                return False
        return True

    def lower(self):
        return self.content.lower()


t = Token("12b")
print(t)
print(repr(t))
print(str(t))