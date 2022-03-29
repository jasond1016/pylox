from .token_type import TokenType
from .expr import Binary, Unary, Literal, Grouping
from .stmt import Print, Expression
import pylox.lox

class Parser:
    current = 0
    def __init__(self, tokens):
        self.tokens = tokens
    
    def parse(self):
        statements = []
        while not self._is_at_end():
            statements.append(self._statement())
        return statements
    
    def _statement(self):
        if self._match(TokenType.PRINT):
            return self._print_statement()
        return self._expression_statement()
    
    def _print_statement(self):
        expr = self.expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(expr)
    
    def _expression_statement(self):
        expr = self.expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)

    def expression(self):
        return self.equality()
    
    def equality(self):
        expr = self.comparison()

        while(self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            operator = self._previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        
        return expr

    def comparison(self):
        expr = self.term()

        while(self._match(TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL)):
            operator = self._previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        
        return expr

    def term(self):
        expr = self.factor()

        while(self._match(TokenType.PLUS, TokenType.MINUS)):
            operator = self._previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        
        return expr

    def factor(self):
        expr = self.unary()

        while(self._match(TokenType.STAR, TokenType.SLASH)):
            operator = self._previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        
        return expr
        
    def unary(self):
        if self._match(TokenType.MINUS, TokenType.BANG):
            operator = self._previous()
            right = self.unary()
            return Unary(operator, right)
        
        return self.primary()
    
    def primary(self):
        if self._match(TokenType.TRUE):
            return Literal(True)
        
        if self._match(TokenType.FALSE):
            return Literal(False)
        
        if self._match(TokenType.NIL):
            return Literal(None)
        
        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)
        
        if self._match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after expression.")
            return Grouping(expr)
        
        raise self._error(self._peek(), "Expect expression.")
    
    def _match(self, *types):
        for type in types:
            if self._check(type):
                self._advance()
                return True
        
        return False
    
    def _check(self, type):
        if self._is_at_end():
            return False
        return self._peek().type == type
    
    def _advance(self):
        if not self._is_at_end():
            self.current += 1
        return self._previous()
    
    def _is_at_end(self):
        return self._peek().type == TokenType.EOF
    
    def _peek(self):
        return self.tokens[self.current]
    
    def _previous(self):
        return self.tokens[self.current - 1]
    
    def _consume(self, type, message):
        if self._check(type):
            return self._advance()
        return self._error(self._peek(), message)
    
    def _error(self, token, message):
        pylox.lox.Lox.error(token, message)
        return ParserError(message)
    
    def _synchronize(self):
        self._advance()
        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return
            
            peek_type = self._peek().type
            if peek_type == TokenType.CLASS or \
               peek_type == TokenType.FUN or \
               peek_type == TokenType.VAR or \
               peek_type == TokenType.FOR or \
               peek_type == TokenType.IF or \
               peek_type == TokenType.WHILE or \
               peek_type == TokenType.PRINT or \
               peek_type == TokenType.RETURN:
               return
            
            self._advance()

class ParserError(Exception):
    pass