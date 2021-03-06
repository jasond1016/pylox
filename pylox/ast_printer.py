from .visitor import Visitor
from .expr import Binary, Grouping, Literal, Unary
from .token import Token
from .token_type import TokenType

class AstPrinter(Visitor):
    def __init__(self):
        pass

    def print(self, expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme ,expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("group" ,expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)
    
    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs) -> str:
        builder = f"({name}"
        for expr in exprs:
            builder += f" {expr.accept(self)}"
        builder += ")"
        return builder
