from .token import Token

class Environment:
    _values = {}

    def define(self, name, value):
        self._values[name] = value

    def get(self, token: Token):
        if token.lexeme in self._values:
            return self._values[token.lexeme]
        else:
            raise RuntimeError(token, f"Undefined variable '{token.lexeme}'.")
    
    def _assign(self, token: Token, value):
        if token.lexeme not in self._values:
            raise RuntimeError(token, f"Undefined variable '{token.lexeme}'.")
        self._values[token.lexeme] = value
        
        return 