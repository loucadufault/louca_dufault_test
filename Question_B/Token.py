class Token:
    def __init__(self, content):
        try:
            self.content =  int(content)
        except ValueError:
            raise ValueError("Token content must be a number composed only of digits.")
    
    def __repr__(self):
        """Representation of the Token object as a string mimicking the contructor call."""
        return "Token({})".format(self.content)

    def __str__(self):
        """String representation of the Token object mimicking the initializer passed to the constructor call."""
        return str(self.content)

    def __int__(self):
        return self.content

    def compare(self, token):   
        return int(self.content) - int(token.content)

t = Token("12")
print(t)
print(repr(t))
print(str(t))