def calcular_percentual_vendas(vendas: tuple, produtos_ids: list) -> list:
    """Calcula o percentual de vendas de cada produto em relação ao total vendido.

    Parâmetros:
        vendas: tupla de tuplas (id_venda, id_produto, quantidade).
        produtos_ids: lista com todos os ids de produtos existentes.

    Retorna:
        list: lista de tuplas (id_produto, percentual) ordenada por id_produto.
    """
    totais = {}
    for pid in produtos_ids:
        totais[pid] = 0

    for id_venda, id_produto, quantidade in vendas:
        if id_produto in totais:
            totais[id_produto] += quantidade

    total_geral = sum(totais.values())

    resultado = []
    for pid in produtos_ids:
        if total_geral == 0:
            resultado.append((pid, 0.0))
        else:
            resultado.append((pid, totais[pid] / total_geral))

    return resultado


def calcular_total_mensal(vendas: tuple) -> float:
    """Soma os valores totais de todas as vendas do mês.

    Parâmetros:
        vendas: tupla de tuplas (id_venda, valor_total).

    Retorna:
        float: soma dos valores de todas as vendas.
    """
    return sum(valor for _, valor in vendas) if vendas else 0.0


def calcular_variacao_mensal(historico: tuple, mes: str):
    """Calcula o percentual de variação de vendas em relação ao mês anterior.

    Parâmetros:
        historico: tupla de tuplas (mes, valor_total).
        mes: mês de referência para o cálculo.

    Retorna:
        float | None: percentual de variação ou None se não houver mês anterior.
    """
    meses = [h[0] for h in historico]
    if mes not in meses:
        return None

    idx = meses.index(mes)
    if idx == 0:
        return None

    valor_atual = historico[idx][1]
    valor_anterior = historico[idx - 1][1]

    if valor_anterior == 0:
        return None

    return ((valor_atual - valor_anterior) / valor_anterior) * 100
