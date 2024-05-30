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

## Interface Streamlit


## Que es pot fer?
Podrem asignar tipus a diferents elements com constants, variables y funcions.
```Haskell
2 :: N
x :: S->S
(+) :: P->P->P
sum :: N->N->N
```
Les funcions es poden definir amb un nom, o es poden utilitzar aquestes funcions algebraiques:
- (+)
- (*)
- (-)
- (/)
- (%)
Aquestes, a diferencia de les funcions amb nom, s'han de posar entre parentesis.

Al asignar un tipus usant el boto **Evaluate** queda registrat en la memoria cache de streamlit. Aquest romandra a la taula fins que parem l'execució del programa o fins que es cliqui el botó **Reset**.

El boto **Reset** buida totes les variables asignades anteriorment per l'usuari.

### Restriccions

S'obtindrà un TypeInferenceError si es defineix un element amb dues vegades (amb tipus diferents)

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

**Tipus Polimorfics**
S'accepten tipus polimorfics com:
```Haskell
2::N
(+) :: a -> a -> a
\x -> (+) 2 x
```
Que inferira l'aplicació com a un tipus N i conseqüentment l'abstracció com a tipus N->N, però si provem amb un altre tipus com:
```Haskell
3::F
(+) :: a -> a -> a
\x -> (+) 2 x
```
El resultat de l'abstracció es F->F.

Inclus es pot propagar el tipus polimorfic:
```Haskell
3::F
(+) :: a -> a -> a
(+) x 2
```
Amb propagar volem dir que el tipus polimorfic es pot utilitzar per inferir sense necessitat d'un tipus definit.

![Poly Propagation](assets/poly_propagation.png)

Com es pot veure la segona aplicació (+) x, no hi ha cap tipus definit aixi que es propaga x como una a, y @ com a->a, y es resol el tipus polimorfic a la següent aplicació.





