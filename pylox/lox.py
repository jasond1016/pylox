import sys
from .scanner import Scanner

class Lox:
    had_error = False

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


    def run_prompt(self):
        while True:
            line = input("> ")
            if line:
                self.run(line)
                Lox.had_error = False

    def run(self, source):
        print(source)
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)

    @staticmethod
    def error(line, message):
        Lox.__report(line, "", message)
    
    @staticmethod
    def __report(line, where, message):
        print("[line " + str(line) + "] Error" + where + ": " + message, file=sys.stderr)
        Lox.had_error = True
