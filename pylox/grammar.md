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
               | equality ;
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
               | printStmt
               | block ;

block          → "{" declaration* "}" ;

exprStmt       → expression ";" ;
printStmt      → "print" expression ";" ;
```
