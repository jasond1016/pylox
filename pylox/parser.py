from .token_type import TokenType
from .expr import Binary, Unary, Literal, Grouping, Variable, Assign, Logical, Call
from .stmt import Block, Print, Expression, Var, If, While
import pylox.lox

class Parser:
    current = 0
    class ParseError(Exception):
        pass

    def __init__(self, tokens):
        self.tokens = tokens
    
    def parse(self):
        statements = []
        while not self._is_at_end():
            statements.append(self._declaration())
        return statements
    
    def _declaration(self):
        try:
            if self._match(TokenType.VAR):
                return self._var_declaration()
            return self._statement()
        except self.ParseError:
            self._synchronize()
            return None
    
    def _var_declaration(self):
        token = self._consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self._match(TokenType.EQUAL):
            initializer = self.expression()
        
        self._consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(token, initializer)

    def _statement(self):
        if self._match(TokenType.FOR):
            return self._for_statement()
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.WHILE):
            return self._while_statement()
        if self._match(TokenType.PRINT):
            return self._print_statement()
        if self._match(TokenType.LEFT_BRACE):
            return Block(self._block_statement())
        return self._expression_statement()
    
    def _for_statement(self):
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        if self._match(TokenType.VAR):
            initializer = self._var_declaration()
        elif self._match(TokenType.SEMICOLON):
            initializer = None
        else:
            initializer = self._expression_statement()
        
        if self._check(TokenType.SEMICOLON):
            condition = None
        else:
            condition = self.expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")
        
        if self._check(TokenType.RIGHT_PAREN):
            increment = None
        else:
            increment = self.expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ';' after for clauses.")

        body = self._statement()
        if increment is not None:
            new_body = []
            new_body.append(body)
            new_body.append(Expression(increment))
            body = Block(new_body)
        
        if condition is None:
            condition = Literal(True)
        body = While(condition, body)
        
        if initializer is not None:
            new_body = []
            new_body.append(Expression(initializer))
            new_body.append(body)
            body = Block(new_body)

        return body

    def _if_statement(self):
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        expr = self.expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
        then_branch = self._statement()
        if self._match(TokenType.ELSE):
            else_branch = self._statement()
        return If(expr, then_branch, else_branch)

    def _while_statement(self):
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        expr = self.expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self._statement()
        return While(expr, body)
        
    def _print_statement(self):
        expr = self.expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(expr)
    
    def _block_statement(self):
        statements = []
        while (not self._check(TokenType.RIGHT_BRACE)) and (not self._is_at_end()):
            statements.append(self._declaration())
        
        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        
        return statements
    
    def _expression_statement(self):
        expr = self.expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)

    def expression(self):
        return self._assignment()
    
    def _assignment(self):
        expr = self._or()

        if self._match(TokenType.EQUAL):
            equals = self._previous()
            value = self._assignment()

            if isinstance(expr, Variable):
                token = expr.name
                return Assign(token, value)
            self._error(equals, "Invalid assignment target.")
        
        return expr
    
    def _or(self):
        expr = self._and()
        while self._match(TokenType.OR):
            operator = self._previous()
            right = self._and()
            expr = Logical(expr, operator, right)
        
        return expr
    
    def _and(self):
        expr = self.equality()
        if self._match(TokenType.AND):
            operator = self._previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        
        return expr

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
        
        return self._call()
    
    def _call(self):
        expr = self.primary()
        while True:
            if self._match(TokenType.LEFT_PAREN):
                expr = self._finish_call(expr)
            else:
                break
        
        return expr
    
    def _finish_call(self, expr):
        arguments = []
        if not self._check(TokenType.RIGHT_BRACE):
            arguments.append(self.expression())
            while self._match(TokenType.COMMA):
                if len(arguments) >= 255:
                    self._error(self._peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
        paren = self._consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return Call(expr, paren, arguments)
    
    def _arguments(self):
        expr = self.expression()
        if self._match(TokenType.LEFT_PAREN):
            while self._match(TokenType.RIGHT_PAREN):
                pass

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
        
        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous())
        
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
        return self.ParseError(message)
    
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

