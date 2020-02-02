class Token:
    def __init__(self, content):
        self.content =  content.lower()
    
    def __repr__(self):
        """Representation of the Token object as a string mimicking the contructor call."""
        return "Token({})".format(self.content)

    def __str__(self):
        """String representation of the Token object mimicking the initializer passed to the constructor call."""
        return self.content
    
    @classmethod
    def compare_alpha(token1, token2):
        i = 0
        while (i < min(len(token1), len(token2))):
            if (token1[i] != token2[i]):
                return ord(token1[i]) - ord(token2[i])
            i += 1
        
        return ord(min(token1, token2, key=len)[i]) - (ord('a') - 1)
    
    @classmethod
    def compare_num(token1, token2):
        return int(self.content) - int(token.content)

    def compare(self, token):
        if (self.content.isalpha() and token.content.isalpha()): # both tokens are entirely alphabetical
            return compare_alpha(self.content, token.content):

        elif (self.content.isdigit() and token.content.isdigit()): # both tokens are entirely numeric
            return int(self.content) - int(token.content)

        else: # either token is alphanumeric
            p = re.compile(r"[^\W\d_]+|\d+")
            self_alphanum = p.findall(self.content) # split tokens into alpha and numeric components
            token_alphanum = p.findall(token.content)

            i = 0
            while (i < min(len(self_alphanum), len(token_alphanum))):
                if (self_alphanum)
                if (self_alphanum[i] != token_alphanum[i]):
                    return ord(token1[i]) - ord(token2[i])
                i += 1
        
            return ord(min(token1, token2, key=len)[i]) - (ord('a') - 1)

    # def isalpha(self):
    #     for char in self.content:
    #         if (not char.isalpha()):
    #             return False
    #     return True

t = Token("12b")
print(t)
print(repr(t))
print(str(t))