from pylox.lox import Lox
from pylox.ast_printer import AstPrinter
from pylox.expr import Binary, Grouping, Literal, Unary
from pylox.token import Token
from pylox.token_type import TokenType

if __name__ == "__main__":
    Lox()
    # expression = Binary(
    #     Unary(
    #         Token(TokenType.MINUS, "-", None, 1),
    #         Literal(123)),
    #     Token(TokenType.STAR, "*", None, 1),
    #     Grouping(
    #         Literal(45.67)))
    # print(AstPrinter().print(expression))
