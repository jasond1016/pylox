import sys

from pylox.token_type import TokenType
from .scanner import Scanner
from .parser import Parser
from .ast_printer import AstPrinter
from pylox.interpreter import Interpreter

class Lox:
    interpreter = Interpreter()
    had_error = False
    had_runtime_error = False

    def __init__(self):
        args = sys.argv
        if len(args) > 2:
            print("Usage: python lox [script]")
            sys.exit(64)
        elif len(args) == 2:
            self.run_file(args[1])
        else:
            self.run_prompt()

    def run_file(self, path):
        with open(path, 'r') as file:
            self.run(file.read())
            if Lox.had_error:
                sys.exit(65)
            if Lox.had_runtime_error:
                sys.exit(70)


    def run_prompt(self):
        while True:
            line = input("> ")
            if line:
                self.run(line)
                Lox.had_error = False

    def run(self, source):
        # print(source)
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        if Lox.had_error:
            return
        self.interpreter.interpret(expression)

    @staticmethod
    def error(line, message):
        Lox.__report(line, "", message)
    
    @staticmethod
    def __report(line, where, message):
        print("[line " + str(line) + "] Error" + where + ": " + message, file=sys.stderr)
        Lox.had_error = True

    @staticmethod
    def error(token, message):
        if token.type == TokenType.EOF:
            Lox.__report(token.line, " at end", message)
        else:
            Lox.__report(token.line, " at '" + token.lexeme + "'", message)

    @staticmethod
    def runtime_error(error):
        print(f"{error.message}\n[line {error.token.line}]", file=sys.stderr)
        Lox.had_runtime_error = True