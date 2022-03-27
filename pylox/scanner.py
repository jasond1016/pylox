from .token_type import TokenType
from .token import Token
import pylox.lox

class Scanner:
    keywords = {
        "and":    TokenType.AND,
        "class":  TokenType.CLASS,
        "else":   TokenType.ELSE,
        "false":  TokenType.FALSE,
        "for":    TokenType.FOR,
        "fun":    TokenType.FUN,
        "if":     TokenType.IF,
        "nil":    TokenType.NIL,
        "or":     TokenType.OR,
        "print":  TokenType.PRINT,
        "return": TokenType.RETURN,
        "super":  TokenType.SUPER,
        "this":   TokenType.THIS,
        "true":   TokenType.TRUE,
        "var":    TokenType.VAR,
        "while":  TokenType.WHILE,
    }
    def __init__(self, source):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []
    
    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scanToken()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self):
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
        elif c == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            return
        elif c == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            return
        elif c == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            return
        elif c == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            return
        elif c == '/':
            if self.match('/'):
                while(self.peek() != '\n' and not self.is_at_end()):
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
            return
        elif c == ' ' or c == '\r' or c == '\t':
            return
        elif c == '\n':
            self.line += 1
            return
        elif c == '"':
            self.string()
        else:
            if self.isDigit(c):
                self.number()
            elif self.isAlpha(c):
                self.identifier()
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

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True
    
    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]
    
    def string(self):
        while(self.peek() != '"' and not self.is_at_end()):
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        
        if self.is_at_end():
            pylox.lox.Lox.error(self.line, "Unterminated string.")
        
        self.advance()
        
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)
    
    def isDigit(self, c):
        return c >= '0' and c <= '9'
    
    def number(self):
        while(self.isDigit(self.peek())):
            self.advance()
        
        if self.peek() == '.' and self.isDigit(self.peek_next()):
            self.advance()
            while(self.isDigit(self.peek())):
                self.advance()
        
        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))    
    def peek_next(self):
        if self.current + 1 > len(self.source):
            return '\0'
        return self.source[self.current + 1]
    
    def isAlpha(self, c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_'
    
    def identifier(self):
        while(self.isAlphaNumeric(self.peek())):
            self.advance()
        
        text = self.source[self.start:self.current]
        type = Scanner.keywords.get(text)
        if (type == None):
            type = TokenType.IDENTIFIER
        self.add_token(type)
    
    def isAlphaNumeric(self, c):
        return self.isAlpha(c) or self.isDigit(c)
