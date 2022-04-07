import os

EXPR = [
    "Assign   | name: Token, value: Expr",
    "Binary   | left: Expr, operator: Token, right: Expr",
    "Call     | callee: Expr, paren: Token, arguments: List[Expr]",
    "Grouping | expression: Expr",
    "Literal  | value",
    "Logical  | left: Expr, operator: Token, right: Expr",
    "Unary    | operator: Token, right: Expr",
    "Variable | name: Token",
]

STMT = [
    "Block      | statements: List[Stmt]",
    "Expression | expression: Expr",
    "Function | name: Token, params: List[Token], body: List[Stmt]",
    "If         | condittion: Expr, then_branch: Stmt, else_branch: Stmt",
    "Print      | expression: Expr",
    "Var        | name: Token, initializer: Expr",
    "While      | condition: Expr, body: Stmt"
]

def define_ast(output_dir, basename, types):
    with open(output_dir, "w") as f:
        f.write("# Auto-generated by tool/generate_ast.py\n")
        f.write("from .token import Token\n")
        if basename == "Stmt":
            f.write("from .expr import Expr\n")
        f.write("from typing import List\n")
        f.write("\n")
        f.write(f"class {basename}:\n")
        f.write("    pass\n")
        f.write("\n")

        for expr in types:
            class_name = expr.split('|', 1)[0].strip()
            fields = expr.split('|', 1)[1].strip()
            f.write(f"class {class_name}({basename}):\n")
            f.write(f"    def __init__(self, {fields}):\n")

            for field in fields.split(','):
                field_name = field.split(":")[0].strip()
                f.write(f"        self.{field_name} = {field_name}\n")
        
            f.write("\n")
            f.write("    def accept(self, visitor):\n")
            f.write(f"        return visitor.visit_{class_name.lower()}_{basename.lower()}(self)\n")
            f.write("\n")

def define_visitor(output_dir, expr_types, stmt_types):
    with open(output_dir, "w") as f:
        f.write("# Auto-generated by tool/generate_ast.py\n")
        f.write("from abc import ABC, abstractmethod\n")
        joined_expr_types = ", ".join([type.split("|")[0].strip() for type in expr_types])
        f.write(f"from .expr import {joined_expr_types}\n")
        joined_stmt_types = ", ".join([type.split("|")[0].strip() for type in stmt_types])
        f.write(f"from .stmt import {joined_stmt_types}\n")
        f.write("\n")
        f.write("class Visitor(ABC):\n")
        f.write("\n")
        for type in expr_types:
            type_name = type.split('|', 1)[0].strip()
            f.write("    @abstractmethod\n")
            f.write(f"    def visit_{type_name.lower()}_expr(self, expr: {type_name}):\n")
            f.write("        pass\n")
            f.write("\n")
        for type in stmt_types:
            type_name = type.split('|', 1)[0].strip()
            f.write("    @abstractmethod\n")
            f.write(f"    def visit_{type_name.lower()}_stmt(self, stmt: {type_name}):\n")
            f.write("        pass\n")
            f.write("\n")

if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    foldername = os.path.join(dirname, '../')
    define_ast(foldername + "expr.py", "Expr", EXPR)
    define_ast(foldername + "stmt.py", "Stmt", STMT)
    define_visitor(foldername + "visitor.py", EXPR, STMT)
