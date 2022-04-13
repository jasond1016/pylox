from codecs import EncodedFile

from pylox.return_exception import ReturnException
from .lox_callable import LoxCallable
from .stmt import Function
from .environment import Environment


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment) -> None:
        self._declaration = declaration
        self._closure = closure

    def call(self, interpreter, arguments):
        environment = Environment(self._closure)
        for i in range(len(self._declaration.params)):
            environment.define(self._declaration.params[i].lexeme, arguments[i])
        
        try:
            interpreter._execute_block(self._declaration.body, environment)
        except ReturnException as return_value:
            return return_value.value
    
    def arity(self):
        return len(self._declaration.params)
    
    def __repr__(self) -> str:
        return f"<fn {self._declaration.name.lexeme}>"