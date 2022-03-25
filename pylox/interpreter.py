from pylox.runtime_exception import RuntimeException
from .visitor import Visitor
from .expr import Binary, Grouping, Literal, Unary
from .token_type import TokenType
import pylox.lox

class Interpreter(Visitor):
    
    def interpret(self, expression):
        try:
            value = self.__evaluate(expression)
            print(self.__stringify(value))
        except RuntimeException as err:
            pylox.lox.Lox.runtime_error(err)

    def visit_binary_expr(self, expr: Binary):
        left = self.__evaluate(expr.left)
        right = self.__evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.type == TokenType.SLASH:
            self.__check_number_operands(expr.operator, left, right)
            # TODO zero division should be considered
            return float(left) / float(right)
        elif expr.operator.type == TokenType.STAR:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.type == TokenType.PLUS:
            self.__check_number_operands(expr.operator, left, right)
            # TODO plus in lox may be different from python
            try:
                return left + right
            except Exception:
                raise RuntimeException(expr.operator, "Operands must be two numbers or two strings.")
        elif expr.operator.type == TokenType.GREATER:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.type == TokenType.LESS:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.type == TokenType.LESS_EQUAL:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return not self.__is_equal(left, right)
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.__is_equal(left, right)

        return None

    def visit_grouping_expr(self, expr: Grouping):
        return self.__evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_unary_expr(self, expr: Unary):
        right = self.__evaluate(expr.right)
        if expr.operator.type == TokenType.BANG:
            return self.__is_truthy(right)
        elif expr.operator.type == TokenType.MINUS:
            self.__check_number_operand(expr.operator, expr.right)
            return -float(right)
        return None

    def __evaluate(self, expr):
        return expr.accept(self)
    
    def __is_truthy(self, object):
        if object is None:
            return False
        elif object == False:
            return False
        else:
            return True
    
    def __is_equal(self, left, right):
        # TODO equal in lox may be different from python
        return left == right
    
    def __check_number_operand(self, operator, operand):
        try:
            float(operand)
        except Exception:
            raise RuntimeException(operator, "Operand must be a number.")

    def __check_number_operands(self, operator, left, right):
        try:
            float(left)
            float(right)
        except Exception:
            raise RuntimeException(operator, "Operands must be numbers.")
    
    def __stringify(self, object):
        if object is None:
            return "nil"
        try:
            # TODO True or False will be converted to number.
            text = str(float(object))
            if text.endswith(".0"):
                text = text[0:len(text)-2]
            return text
        except Exception:
            pass

        return str(object)