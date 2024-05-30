# Practica Llenguatges de Programació (LP) 2023-2024 Q2
## L'analitzador de tipus HinNer

Aquest projecte es un senzill programa d'analitzador de tipus d'expresions. Fet a partir d'una gramatica [ANTLR4](https://www.antlr.org/) s'ha implementat en Python un visitador que donada una expressió infereix el seu tipus, en el cas de que no ho sigui mostrant el error de tipus que existeix. A més es pot asignar tipus a funcions, variables y constants per tal d'inferir el tipus d'una expressió d'una forma més completa

## Dependencies

Per correr aquest programa es necesari Python y ANTLR4, que es pot obtenir d'aquesta forma (en Linux i macOS)

```cmd
pip install antlr4-tools

antlr4

pip install antlr4-python3-runtime
```

A més caldra `streamlit` i `pandas`. Es poden instalar executan:
```cmd
pip install streamlit

pip install pandas
```

## Execució

Per executar aquest programa s'ha proporcionat un `Makefile` amb 3 regles:
- **all**: 	:warning: Aquesta regla fara de la gramatica un lexer, un parser i un **visitor**. Per tant eliminar el visitor proporcionat. Esta pensat per noves implementacions

- **novisitor**: Aquesta regla fara de la gramatica un lexer i un parser corresponent, però no fara un nou visitor.

- **run**: Corre l'aplicació mitjançant streamlit.

## Que es pot fer?

### Casos del enunciat
**Aplicacions:**
```Haskell
2 :: N
sum :: N->N->N
(+) :: N->N->N
(+) 2 x
sum 2 x
```
**Abstraccions:**
```Haskell
2 :: N
sum :: N->N->N
(+) :: N->N->N
\x -> (+) 2 x
\x -> sum 2 x
```

### Extra
**Aplicacion anidada:**
```Haskell
1::N
2::N
3::N
(+) :: N->N->N
(\z -> (+) ((+) 1 2) z)
Combinacio d'aplicacions mirar
```
**Combinacio d'aplicacions**
Per aquest cas necesitem una doble pasada del algoritme d'inferencia per inferir del tot el tipus de la expressió
```Haskell
2::N
(+) :: N->N->N
(*) :: N->N->N
(+) ((*) 2 x) ((+) 2 2)
```

O per el cas d'una aplicació
```Haskell
2::N
(+) :: N->N->N
(*) :: N->N->N
\x -> (+) ((*) 2 x) ((+) 2 2)
```

### Restriccions

S'obtindrà un TypeInferenceError si es defineix una element com amb mes de dos tipus.


