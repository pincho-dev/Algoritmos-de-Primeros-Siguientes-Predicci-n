

# --- Gramatica 1 ---
# S -> A uno B C | S dos
# A -> B C D | A tres | eps
# B -> D cuatro C tres | eps
# C -> cinco D B | eps
# D -> seis | eps

grammar1 = {
    "S": [["A", "uno", "B", "C"], ["S", "dos"]],
    "A": [["B", "C", "D"], ["A", "tres"], []],
    "B": [["D", "cuatro", "C", "tres"], []],
    "C": [["cinco", "D", "B"], []],
    "D": [["seis"], []],
}

nonterminals1 = {"S", "A", "B", "C", "D"}
terminals1 = {"uno", "dos", "tres", "cuatro", "cinco", "seis"}
start1 = "S"


# --- Gramatica 2 ---
# S -> A B uno
# A -> dos B | eps
# B -> C D | tres | eps
# C -> cuatro A B | cinco
# D -> seis | eps

grammar2 = {
    "S": [["A", "B", "uno"]],
    "A": [["dos", "B"], []],
    "B": [["C", "D"], ["tres"], []],
    "C": [["cuatro", "A", "B"], ["cinco"]],
    "D": [["seis"], []],
}

nonterminals2 = {"S", "A", "B", "C", "D"}
terminals2 = {"uno", "dos", "tres", "cuatro", "cinco", "seis"}
start2 = "S"


EPSILON = "e"  # simbolo interno para representar epsilon dentro de un conjunto


def primeros(grammar, nonterminals, terminals):
    
    primeros_dict = {nt: set() for nt in nonterminals}
    changed = True
    while changed:
        changed = False
        for head, productions in grammar.items():
            for prod in productions:
                if prod == []:
                    if EPSILON not in primeros_dict[head]:
                        primeros_dict[head].add(EPSILON)
                        changed = True
                    continue

                nullable_prefix = True
                for symbol in prod:
                    if symbol in terminals:
                        if symbol not in primeros_dict[head]:
                            primeros_dict[head].add(symbol)
                            changed = True
                        nullable_prefix = False
                        break
                    else:
                        before = len(primeros_dict[head])
                        primeros_dict[head] |= (primeros_dict[symbol] - {EPSILON})
                        if len(primeros_dict[head]) != before:
                            changed = True
                        if EPSILON not in primeros_dict[symbol]:
                            nullable_prefix = False
                            break

                if nullable_prefix:
                    if EPSILON not in primeros_dict[head]:
                        primeros_dict[head].add(EPSILON)
                        changed = True
    return primeros_dict


def primeros_de_secuencia(seq, primeros_dict, terminals):
    """PRIMEROS de una secuencia de simbolos (util para SIGUIENTES y PREDICCION)."""
    result = set()
    nullable = True
    for symbol in seq:
        if symbol in terminals:
            result.add(symbol)
            nullable = False
            break
        else:
            result |= (primeros_dict[symbol] - {EPSILON})
            if EPSILON not in primeros_dict[symbol]:
                nullable = False
                break
    if nullable:
        result.add(EPSILON)
    return result


def siguientes(grammar, nonterminals, terminals, start, primeros_dict):
    """SIGUIENTES(X) para cada no terminal X. Algoritmo de punto fijo."""
    siguientes_dict = {nt: set() for nt in nonterminals}
    siguientes_dict[start].add("$")
    changed = True
    while changed:
        changed = False
        for head, productions in grammar.items():
            for prod in productions:
                for i, symbol in enumerate(prod):
                    if symbol not in nonterminals:
                        continue
                    resto = prod[i + 1:]
                    first_resto = (
                        primeros_de_secuencia(resto, primeros_dict, terminals)
                        if resto else {EPSILON}
                    )
                    before = len(siguientes_dict[symbol])
                    siguientes_dict[symbol] |= (first_resto - {EPSILON})
                    if EPSILON in first_resto:
                        siguientes_dict[symbol] |= siguientes_dict[head]
                    if len(siguientes_dict[symbol]) != before:
                        changed = True
    return siguientes_dict


def prediccion(grammar, primeros_dict, siguientes_dict, terminals):
    """PREDICCION(A -> alpha) para cada produccion de la gramatica."""
    prediccion_dict = {}
    for head, productions in grammar.items():
        for idx, prod in enumerate(productions):
            first_prod = (
                {EPSILON} if prod == []
                else primeros_de_secuencia(prod, primeros_dict, terminals)
            )
            resultado = first_prod - {EPSILON}
            if EPSILON in first_prod:
                resultado |= siguientes_dict[head]
            prediccion_dict[(head, idx)] = resultado
    return prediccion_dict


def mostrar(nombre, grammar, nonterminals, terminals, start):
    pr = primeros(grammar, nonterminals, terminals)
    si = siguientes(grammar, nonterminals, terminals, start, pr)
    pe = prediccion(grammar, pr, si, terminals)

    print(f"=== {nombre} ===")
    print("PRIMEROS:")
    for nt in sorted(nonterminals):
        print(f"  {nt}: {sorted(pr[nt])}")
    print("SIGUIENTES:")
    for nt in sorted(nonterminals):
        print(f"  {nt}: {sorted(si[nt])}")
    print("PREDICCION:")
    for (head, idx), conjunto in pe.items():
        prod = grammar[head][idx]
        prod_str = " ".join(prod) if prod else "eps"
        print(f"  {head} -> {prod_str}: {sorted(conjunto)}")
    print()


if __name__ == "__main__":
    mostrar("Gramatica 1", grammar1, nonterminals1, terminals1, start1)
    mostrar("Gramatica 2", grammar2, nonterminals2, terminals2, start2)
