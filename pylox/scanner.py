from .token_type import TokenType
from .token import Token
import pylox.lox

class Scanner:
    def __init__(self, source):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []
    
    def scan_tokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def isAtEnd(self):
        return self.current >= len(self.source)
    
    def scanToken(self):
        c = self.advance()
        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
            return
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
            return
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
            return
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
            return
        elif c == ',':
            self.add_token(TokenType.COMMA)
            return
        elif c == '.':
            self.add_token(TokenType.DOT)
            return
        elif c == '-':
            self.add_token(TokenType.MINUS)
            return
        elif c == '+':
            self.add_token(TokenType.PLUS)
            return
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
            return
        elif c == '*':
            self.add_token(TokenType.STAR)
            return
        else:
            pylox.lox.Lox.error(self.line, "Unexpceted character.")
            return

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c
    
    def add_token(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

