from .token import Token

class Environment:
    
    def __init__(self, enclosing=None):
        self._enclosing = enclosing
        self._values = {}

    def define(self, name, value):
        self._values[name] = value

    def get(self, token: Token):
        if token.lexeme in self._values:
            return self._values[token.lexeme]
        
        if self._enclosing:
            return self._enclosing.get(token)
        
        raise RuntimeError(token, f"Undefined variable '{token.lexeme}'.")
    
    def _assign(self, token: Token, value):
        if token.lexeme in self._values:
            self._values[token.lexeme] = value
            return
        
        if self._enclosing:
            self._enclosing._assign(token, value)
            return
        
        raise RuntimeError(token, f"Undefined variable '{token.lexeme}'.")
