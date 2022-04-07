from pylox.lox_callable import LoxCallable
from pylox.lox_function import LoxFunction
from pylox.runtime_exception import RuntimeException
from .visitor import Visitor
from .expr import Assign, Binary, Grouping, Literal, Unary, Variable, Logical, Call
from .stmt import Stmt, Print, Expression, Var, Block, If, While, Function
from .token_type import TokenType
from .environment import Environment
from typing import List
import pylox.lox
import time

class Interpreter(Visitor):

    _globals = Environment()
    _environment = _globals

    def __init__(self):
        class Clock(LoxCallable):

            def call(self, interpreter, arguments):
                return time.time() / 1000

            def arity(self):
                return 0
            
            def __repr__(self) -> str:
                return "<native fn>"

        self._globals.define("clock", Clock())
    
    def interpret(self, statements):
        try:
            for statement in statements:
                self._execute(statement)
        except RuntimeException as err:
            pylox.lox.Lox.runtime_error(err)

    def visit_binary_expr(self, expr: Binary):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self._check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.type == TokenType.SLASH:
            self._check_number_operands(expr.operator, left, right)
            if self._is_equal(right, 0):
                return None
            return float(left) / float(right)
        elif expr.operator.type == TokenType.STAR:
            self._check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.type == TokenType.PLUS:
            if (isinstance(left, (int, float)) and isinstance(right, (int, float))) or \
                (isinstance(left, str) and isinstance(right, str)):
                return left + right
            raise RuntimeException(expr.operator, "Operands must be two numbers or two strings.")
        elif expr.operator.type == TokenType.GREATER:
            self._check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.type == TokenType.LESS:
            self._check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.type == TokenType.LESS_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self._is_equal(left, right)

        return None
    
    def visit_call_expr(self, expr: Call):
        callee = self._evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self._evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise RuntimeException(expr.paren, "Can only call functions and classes.")
        
        function = callee
        if len(arguments) != function.arity():
            raise RuntimeException(expr.paren, f"Expected {function.arity()} arguments but got {len(arguments)}.")
        return function.call(self, arguments)

    def visit_grouping_expr(self, expr: Grouping):
        return self._evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return expr.value
    
    def visit_logical_expr(self, expr: Logical):
        left = self._evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self._is_truthy(left):
                return left
        else:
            if not self._is_truthy(left):
                return left
        return self._evaluate(expr.right)

    def visit_unary_expr(self, expr: Unary):
        right = self._evaluate(expr.right)
        if expr.operator.type == TokenType.BANG:
            return self._is_truthy(right)
        elif expr.operator.type == TokenType.MINUS:
            self._check_number_operand(expr.operator, expr.right)
            return -float(right)
        return None
    
    def visit_variable_expr(self, expr: Variable):
        return self._environment.get(expr.name)
    
    def visit_if_stmt(self, stmt: If):
        if self._is_truthy(stmt.condittion):
            self._execute(stmt.then_branch)
        elif stmt.else_branch:
            self._execute(stmt.else_branch)

    def visit_print_stmt(self, stmt: Expression):
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))
    
    def visit_block_stmt(self, stmt: Block):
        self._execute_block(stmt.statements, Environment(self._environment))

    def visit_expression_stmt(self, stmt: Expression):
        self._evaluate(stmt.expression)
    
    def visit_function_stmt(self, stmt: Function):
        function = LoxFunction(stmt)
        self._environment.define(stmt.name.lexeme, function)

    def visit_var_stmt(self, stmt: Var):
        name = stmt.name
        value = None
        if stmt.initializer:
            value = self._evaluate(stmt.initializer)
        self._environment.define(name.lexeme, value)
    
    def visit_while_stmt(self, stmt: While):
        while self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.body)

    def visit_assign_expr(self, expr: Assign):
        value = self._evaluate(expr.value)
        self._environment._assign(expr.name, value)
        return value

    def _execute(self, stmt):
        stmt.accept(self)
    
    def _execute_block(self, statements: List[Stmt], environment: Environment):
        previous = self._environment
        try:
            self._environment = environment
            for statement in statements:
                self._execute(statement)
        finally:
            self._environment = previous

    def _evaluate(self, expr):
        return expr.accept(self)
    
    def _is_truthy(self, object):
        if object is None:
            return False
        elif object == False:
            return False
        else:
            return True
    
    def _is_equal(self, left, right):
        # TODO equal in lox may be different from python
        return left == right
    
    def _check_number_operand(self, operator, operand):
        if not isinstance(operand, (int, float)):
            raise RuntimeException(operator, "Operand must be a number.")

    def _check_number_operands(self, operator, left, right):
        if not isinstance(left, (int, float)) or \
            not isinstance(right, (int, float)):
            raise RuntimeException(operator, "Operand must be a number.")
    
    def _stringify(self, object):
        if object is None:
            return "nil"
        
        if isinstance(object, float):
            text = str(float(object))
            if text.endswith(".0"):
                text = text[0:len(text)-2]
            return text

        return str(object)