def verificar_reposicao(produtos: tuple) -> int:
    """Retorna a quantidade de produtos que precisam de reposição (quantidade < 5).

    Parâmetros:
        produtos: tupla de tuplas (nome, quantidade).

    Retorna:
        int: quantidade de produtos com quantidade < 5.

    Levanta:
        ValueError: se alguma quantidade for negativa.
    """
    count = 0
    for nome, quantidade in produtos:
        if quantidade < 0:
            raise ValueError("Dado inválido")
        if quantidade < 5:
            count += 1
    return count
