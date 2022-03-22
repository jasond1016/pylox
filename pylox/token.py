class Token:
    def __init__(self, type, lexme, literal, line):
        self.type = type
        self.lexme = lexme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return str(self.type) + " " + self.lexme + " " + ("" if self.literal == None else str(self.literal))
