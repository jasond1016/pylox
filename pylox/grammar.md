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
               | call
call           → primary ( "(" arguments? ")" )* ;
arguments      → expression ( "," expression )* ;
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")"
               | IDENTIFIER ;
```

---
Statements
```
program        → declaration* EOF ;

declaration    → funDecl
               | varDecl
               | statement ;

funDecl        → "fun" function ;

function       → IDENTIFIER "(" parameters? ")" block ;

parameters     → IDENTIFIER ( "," IDENTIFIER )* ;

varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;

statement      → exprStmt
               | forStmt
               | ifStmt
               | printStmt
               | returnStmt
               | whileStmt
               | block ;

exprStmt       → expression ";" ;

ifStmt         → "if" "(" expression ")" statement
               ( "else" statement )? ;

forStmt        → "for" "(" ( varDecl | exprStmt | ";" )
                expression? ";"
                expression? ")"
                statement ;

printStmt      → "print" expression ";" ;

returnStmt     → "return" expression? ";" ;

whileStmt      → "while" "(" expression ")" statement

block          → "{" declaration* "}" ;

```
