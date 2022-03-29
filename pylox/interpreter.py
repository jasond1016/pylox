from pylox.runtime_exception import RuntimeException
from .visitor import Visitor
from .expr import Binary, Grouping, Literal, Unary
from .stmt import Print, Expression
from .token_type import TokenType
import pylox.lox

class Interpreter(Visitor):
    
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

    def visit_grouping_expr(self, expr: Grouping):
        return self._evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_unary_expr(self, expr: Unary):
        right = self._evaluate(expr.right)
        if expr.operator.type == TokenType.BANG:
            return self._is_truthy(right)
        elif expr.operator.type == TokenType.MINUS:
            self._check_number_operand(expr.operator, expr.right)
            return -float(right)
        return None
    
    def visit_print_stmt(self, stmt: Expression):
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))

    def visit_expression_stmt(self, stmt: Expression):
        self._evaluate(stmt.expression)

    def _execute(self, stmt):
        stmt.accept(self)

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