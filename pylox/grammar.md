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
expression     → equality
equality       → comparison ( ( "==" | "!=" ) comparison )* ;
comparison     → term ( ( "<" | "<=" | ">" | ">=" ) term )* ;
term           → factor ( ( "+" | "-" ) factor )* ;
factor         → unary ( ( "*" | "/" ) unary )* ;
unary          → ( "-" | "!" ) unary
               | primary
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")" ;
```

---
Statements
```
program        → statement* EOF ;

statement      → exprStmt
               | printStmt ;

exprStmt       → expression ";" ;
printStmt      → "print" expression ";" ;
```