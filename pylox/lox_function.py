from codecs import EncodedFile
from .lox_callable import LoxCallable
from .stmt import Function
from .environment import Environment


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function) -> None:
        self._declaration = declaration

    def call(self, interpreter, arguments):
        environment = Environment(interpreter._globals)
        for i in range(len(self._declaration.params)):
            environment.define(self._declaration.params[i].lexeme, arguments[i])
        
        interpreter._execute_block(self._declaration.body, environment)
    
    def arity(self):
        return len(self._declaration.params)
    
    def __repr__(self) -> str:
        return f"<fn {self._declaration.name.lexeme}>"