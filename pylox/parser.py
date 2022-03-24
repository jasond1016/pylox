from .token_type import TokenType
from .expr import Binary, Unary, Literal, Grouping
import pylox.lox

class Parser:
    current = 0
    def __init__(self, tokens):
        self.tokens = tokens
    
    def parse(self):
        try:
            return self.expression()
        except ParserError:
            return None
    
    def expression(self):
        return self.equality()
    
    def equality(self):
        expr = self.comparison()

        while(self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            operator = self.__previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        
        return expr

    def comparison(self):
        expr = self.term()

        while(self.__match(TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL)):
            operator = self.__previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        
        return expr

    def term(self):
        expr = self.factor()

        while(self.__match(TokenType.PLUS, TokenType.MINUS)):
            operator = self.__previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        
        return expr

    def factor(self):
        expr = self.unary()

        while(self.__match(TokenType.STAR, TokenType.SLASH)):
            operator = self.__previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        
        return expr
        
    def unary(self):
        if self.__match(TokenType.MINUS, TokenType.BANG):
            operator = self.__previous()
            right = self.unary()
            return Unary(operator, right)
        
        return self.primary()
    
    def primary(self):
        if self.__match(TokenType.TRUE):
            return Literal(True)
        
        if self.__match(TokenType.FALSE):
            return Literal(False)
        
        if self.__match(TokenType.NIL):
            return Literal(None)
        
        if self.__match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.__previous().literal)
        
        if self.__match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.__consume(TokenType.RIGHT_PAREN, "Expected ')' after expression.")
            return Grouping(expr)
        
        raise self.__error(self.__peek(), "Expect expression.")
    
    def __match(self, *types):
        for type in types:
            if self.__check(type):
                self.__advance()
                return True
        
        return False
    
    def __check(self, type):
        if self.__isAtEnd():
            return False
        return self.__peek().type == type
    
    def __advance(self):
        if not self.__isAtEnd():
            self.current += 1
        return self.__previous()
    
    def __isAtEnd(self):
        return self.__peek().type == TokenType.EOF
    
    def __peek(self):
        return self.tokens[self.current]
    
    def __previous(self):
        return self.tokens[self.current - 1]
    
    def __consume(self, type, message):
        if self.__check(type):
            return self.__advance()
        return self.__error(self.__peek(), message)
    
    def __error(self, token, message):
        pylox.lox.Lox.error(token, message)
        return ParserError(message)
    
    def __synchronize(self):
        self.__advance()
        while not self.__isAtEnd():
            if self.__previous().type == TokenType.SEMICOLON:
                return
            
            peek_type = self.__peek().type
            if peek_type == TokenType.CLASS or \
               peek_type == TokenType.FUN or \
               peek_type == TokenType.VAR or \
               peek_type == TokenType.FOR or \
               peek_type == TokenType.IF or \
               peek_type == TokenType.WHILE or \
               peek_type == TokenType.PRINT or \
               peek_type == TokenType.RETURN:
               return
            
            self.__advance()

class ParserError(Exception):
    pass