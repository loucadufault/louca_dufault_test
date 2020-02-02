class Tester:
    def __init__(self, name, cases, oracles):
        self.name = name
        self.cases = cases
        self.oracles = oracles
        self.results = {"pass": 0, "fail": 0}