```
expression     → literal
               | unary
               | binary
               | grouping ;
```

```
literal        → NUMBER | STRING | "true" | "false" | "nil" ;  
grouping       → "(" expression ")" ;  
unary          → ( "-" | "!" ) expression ;  
binary         → expression operator expression ;  
operator       → "==" | "!=" | "<" | "<=" | ">" | ">="  
               | "+"  | "-"  | "*" | "/" ;  
```
---

| Name | Operators | Associates |
| ---- | --------- |----------- |
| Equality | == != | Left |
| Comparison | > >= < <= | Left |
| Term | - + | Left |
| Factor | / * | Left |
| Unary | ! - | Right |

```
expression     → assignment ;
assignment     → IDENTIFIER "=" assignment
               | logic_or ;
logic_or       → logic_and "or" ( logic_and )* ;
logic_and      → equality "and" ( equality )* ;
equality       → comparison ( ( "==" | "!=" ) comparison )* ;
comparison     → term ( ( "<" | "<=" | ">" | ">=" ) term )* ;
term           → factor ( ( "+" | "-" ) factor )* ;
factor         → unary ( ( "*" | "/" ) unary )* ;
unary          → ( "-" | "!" ) unary
               | primary
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")"
               | IDENTIFIER ;
```

---
Statements
```
program        → declaration* EOF ;

declaration    → varDecl
               | statement ;

varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;

statement      → exprStmt
               | ifStmt
               | printStmt
               | whileStmt
               | block ;

ifStmt         → "if" "(" expression ")" statement
               ( "else" statement )? ;

whileStmt      → "while" "(" expression ")" statement

block          → "{" declaration* "}" ;

exprStmt       → expression ";" ;
printStmt      → "print" expression ";" ;
```
