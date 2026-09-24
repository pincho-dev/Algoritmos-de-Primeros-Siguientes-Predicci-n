# Taller: PRIMEROS, SIGUIENTES y PREDICCIÓN

Cálculo analítico e implementación en Python de los conjuntos PRIMEROS,
SIGUIENTES y PREDICCIÓN para las dos gramáticas del taller.

- Santiago Ortegon
- Juan Pablo Orjuela
- Julian Beltran Rodriguez
## Gramáticas

**Gramática 1**

```
S -> A uno B C | S dos
A -> B C D | A tres | eps
B -> D cuatro C tres | eps
C -> cinco D B | eps
D -> seis | eps
```

**Gramática 2**

```
S -> A B uno
A -> dos B | eps
B -> C D | tres | eps
C -> cuatro A B | cinco
D -> seis | eps
```

No terminales: `S, A, B, C, D`. Terminales: `uno, dos, tres, cuatro, cinco, seis`.

## Cómo correr el código

```
python3 taller_ll1.py
```

Imprime PRIMEROS, SIGUIENTES y PREDICCIÓN de las dos gramáticas.

## Algoritmos (resumen)

- **PRIMEROS(X)**: terminales con los que puede empezar cualquier cadena
  derivada de X (incluye ε si X puede desvanecerse). Se calcula por punto
  fijo: se recorren todas las producciones repetidamente hasta que ninguna
  vuelta agregue símbolos nuevos.
- **SIGUIENTES(X)**: terminales que pueden aparecer justo después de X en
  alguna forma derivable desde el símbolo inicial. También es punto fijo,
  porque SIGUIENTES de un no terminal puede depender del SIGUIENTES de otro
  (dependencias circulares).
- **PREDICCIÓN(A -> α)**: PRIMEROS(α) si ε no está en PRIMEROS(α); si ε sí
  está, es (PRIMEROS(α) - {ε}) ∪ SIGUIENTES(A). Indica con qué token de
  entrada un parser LL(1) debe elegir esa producción.

## Resultados — Gramática 1

**PRIMEROS**

| No terminal | PRIMEROS |
|---|---|
| D | {seis, ε} |
| C | {cinco, ε} |
| B | {cuatro, seis, ε} |
| A | {cuatro, cinco, seis, tres, ε} |
| S | {uno, cuatro, cinco, seis, tres} |

**SIGUIENTES**

| No terminal | SIGUIENTES |
|---|---|
| S | {$, dos} |
| A | {uno, tres} |
| B | {$, dos, uno, tres, cinco, seis} |
| C | {$, dos, uno, tres, seis} |
| D | {$, dos, uno, tres, cuatro, seis} |

**PREDICCIÓN**

| Regla | PREDICCIÓN |
|---|---|
| S → A uno B C | {cuatro, cinco, seis, tres, uno} |
| S → S dos | {cuatro, cinco, seis, tres, uno} |
| A → B C D | {cuatro, cinco, seis, tres, uno} |
| A → A tres | {cuatro, cinco, seis, tres} |
| A → ε | {tres, uno} |
| B → D cuatro C tres | {cuatro, seis} |
| B → ε | {$, cinco, dos, seis, tres, uno} |
| C → cinco D B | {cinco} |
| C → ε | {$, dos, seis, tres, uno} |
| D → seis | {seis} |
| D → ε | {$, cuatro, dos, seis, tres, uno} |

**¿Es LL(1)?** No. `S → A uno B C` y `S → S dos` tienen PREDICCIÓN idéntico,
y `A → B C D` se solapa con `A → A tres`. Es consecuencia directa de la
recursión izquierda (`S → S dos`, `A → A tres`): un parser descendente
recursivo no puede decidir con 1 token de lookahead.

## Resultados — Gramática 2

**PRIMEROS**

| No terminal | PRIMEROS |
|---|---|
| C | {cuatro, cinco} |
| D | {seis, ε} |
| B | {cuatro, cinco, tres, ε} |
| A | {dos, ε} |
| S | {dos, cuatro, cinco, tres, uno} |

**SIGUIENTES**

| No terminal | SIGUIENTES |
|---|---|
| S | {$} |
| A | {cuatro, cinco, tres, uno, seis} |
| B | {cuatro, cinco, tres, uno, seis} |
| C | {cuatro, cinco, tres, uno, seis} |
| D | {cuatro, cinco, tres, uno, seis} |

Los cuatro no terminales A, B, C, D terminan con el mismo SIGUIENTES por la
dependencia circular A → C (vía `C → cuatro A B`) → B (vía `B → C D`) → A
(vía `S → A B uno` / `C → cuatro A B`).

**PREDICCIÓN**

| Regla | PREDICCIÓN |
|---|---|
| S → A B uno | {dos, cuatro, cinco, tres, uno} |
| A → dos B | {dos} |
| A → ε | {cuatro, cinco, tres, uno, seis} |
| B → C D | {cuatro, cinco} |
| B → tres | {tres} |
| B → ε | {cuatro, cinco, tres, uno, seis} |
| C → cuatro A B | {cuatro} |
| C → cinco | {cinco} |
| D → seis | {seis} |
| D → ε | {cuatro, cinco, tres, uno, seis} |

**¿Es LL(1)?** No. En `B` las tres producciones se solapan entre sí
(`B → ε` con `B → C D` en {cuatro, cinco}, y con `B → tres` en {tres}), y en
`D`, `D → seis` se solapa con `D → ε` en {seis}. No hay recursión izquierda
aquí; el conflicto viene de las producciones ε cuyo SIGUIENTES se solapa
con el PRIMEROS de otra alternativa del mismo no terminal.

## Comparación

- Misma cantidad de no terminales/terminales y estructura similar (S
  depende de A, B, C; D es hoja), pero G1 tiene recursión izquierda
  explícita y G2 no.
- El tipo de conflicto LL(1) es distinto: en G1 es por recursión izquierda
  (se resolvería con la transformación estándar recursión-izq →
  recursión-der); en G2 es por ambigüedad de producciones ε.
- En G1 los SIGUIENTES de cada no terminal son distintos entre sí; en G2
  colapsan los cuatro no terminales intermedios al mismo conjunto por la
  dependencia circular A↔B↔C.
- Ninguna de las dos gramáticas es LL(1) tal como está escrita.
