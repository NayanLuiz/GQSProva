import unittest

from estoque import verificar_reposicao
from vendas import (
    calcular_percentual_vendas,
    calcular_total_mensal,
    calcular_variacao_mensal,
)


class TestVerificarReposicao(unittest.TestCase):
    """Testes para a função verificar_reposicao(produtos).

    Retorna a quantidade de produtos com quantidade < 5 (precisam de reposição).
    """

    def test_lista_com_produto_em_reposicao(self):
        """Lista mista: um produto com quantidade < 5 deve ser identificado."""
        produtos = (('Shampoo', 10), ('Condicionador', 5), ('Sabonete', 2))
        resultado = verificar_reposicao(produtos)
        self.assertEqual(resultado, 1)

    def test_lista_vazia(self):
        """Lista vazia deve retornar 0 produtos para reposição."""
        produtos = ()
        resultado = verificar_reposicao(produtos)
        self.assertEqual(resultado, 0)

    def test_todos_com_quantidade_suficiente(self):
        """Todos os produtos com quantidade >= 5 não precisam de reposição.

        Quantidade exatamente igual a 5 não dispara reposição (condição é < 5).
        """
        produtos = (('Shampoo', 10), ('Condicionador', 7), ('Sabonete', 5))
        resultado = verificar_reposicao(produtos)
        self.assertEqual(resultado, 0)

    def test_todos_precisam_reposicao(self):
        """Todos os produtos com quantidade < 5 devem ser contados."""
        produtos = (('Shampoo', 1), ('Condicionador', 3), ('Sabonete', 0))
        resultado = verificar_reposicao(produtos)
        self.assertEqual(resultado, 3)

    def test_entrada_invalida_quantidade_negativa(self):
        """Quantidade negativa deve lançar exceção com mensagem 'Dado inválido'."""
        produtos = (('Shampoo', -2), ('Condicionador', 3))
        with self.assertRaises(ValueError) as ctx:
            verificar_reposicao(produtos)
        self.assertEqual(str(ctx.exception), 'Dado inválido')


class TestCalcularPercentualVendas(unittest.TestCase):
    """Testes para a função calcular_percentual_vendas(vendas, produtos_ids).

    Retorna o percentual de venda de cada produto em relação ao total de
    unidades vendidas. Produtos sem vendas recebem percentual 0.0.
    """

    def test_lista_normal_com_produto_sem_vendas(self):
        """Calcula percentuais corretamente; produto 4 sem vendas recebe 0.0.

        Total vendido: 4+3+1+3 = 11 unidades.
        Produto 1: 4 (venda 1) + 3 (venda 2) = 7 → 7/11 ≈ 0.6364
        Produto 2: 3 (venda 1) = 3             → 3/11 ≈ 0.2727
        Produto 3: 1 (venda 1) = 1             → 1/11 ≈ 0.0909
        Produto 4: sem vendas                  → 0/11 = 0.0
        """
        vendas = ((1, 1, 4), (1, 2, 3), (1, 3, 1), (2, 1, 3))
        produtos_ids = [1, 2, 3, 4]
        resultado = calcular_percentual_vendas(vendas, produtos_ids)
        resultado_dict = dict(resultado)
        self.assertAlmostEqual(resultado_dict[1], 7 / 11, places=4)
        self.assertAlmostEqual(resultado_dict[2], 3 / 11, places=4)
        self.assertAlmostEqual(resultado_dict[3], 1 / 11, places=4)
        self.assertAlmostEqual(resultado_dict[4], 0.0, places=4)

    def test_lista_de_vendas_vazia(self):
        """Lista de vendas vazia deve retornar 0.0 para todos os produtos."""
        vendas = ()
        produtos_ids = [1, 2, 3]
        resultado = calcular_percentual_vendas(vendas, produtos_ids)
        for _, percentual in resultado:
            self.assertEqual(percentual, 0.0)

    def test_apenas_um_produto_vendido(self):
        """Único produto disponível e vendido deve ter 100% das vendas."""
        vendas = ((1, 1, 5),)
        produtos_ids = [1]
        resultado = calcular_percentual_vendas(vendas, produtos_ids)
        resultado_dict = dict(resultado)
        self.assertAlmostEqual(resultado_dict[1], 1.0, places=4)

    def test_dois_produtos_mesmo_percentual(self):
        """Dois produtos com mesma quantidade total vendida devem ter 50% cada."""
        vendas = ((1, 1, 3), (1, 2, 3))
        produtos_ids = [1, 2]
        resultado = calcular_percentual_vendas(vendas, produtos_ids)
        resultado_dict = dict(resultado)
        self.assertAlmostEqual(resultado_dict[1], 0.5, places=4)
        self.assertAlmostEqual(resultado_dict[2], 0.5, places=4)

    def test_vendas_diferentes_mesma_quantidade(self):
        """Vendas distintas com mesma quantidade por produto: percentuais iguais."""
        vendas = ((1, 1, 2), (2, 2, 2), (3, 3, 2))
        produtos_ids = [1, 2, 3]
        resultado = calcular_percentual_vendas(vendas, produtos_ids)
        resultado_dict = dict(resultado)
        self.assertAlmostEqual(resultado_dict[1], 1/3, places=4)
        self.assertAlmostEqual(resultado_dict[2], 1/3, places=4)
        self.assertAlmostEqual(resultado_dict[3], 1/3, places=4)

    def test_mesmo_produto_vendas_distintas(self):
        """Mesmo produto em vendas distintas: soma das quantidades = 100%."""
        vendas = ((1, 1, 2), (2, 1, 8))
        produtos_ids = [1]
        resultado = calcular_percentual_vendas(vendas, produtos_ids)
        resultado_dict = dict(resultado)
        self.assertAlmostEqual(resultado_dict[1], 1.0, places=4)


class TestCalcularTotalMensal(unittest.TestCase):
    """Testes para a função calcular_total_mensal(vendas).

    Recebe uma lista de (id_venda, valor_total) e retorna a soma dos valores.
    """

    def test_lista_normal_de_vendas(self):
        """Soma correta de múltiplas vendas (50.50+200.95+20.95+100.40=372.80)."""
        vendas = ((1, 50.50), (2, 200.95), (3, 20.95), (4, 100.40))
        resultado = calcular_total_mensal(vendas)
        self.assertAlmostEqual(resultado, 372.80, places=2)

    def test_lista_de_vendas_vazia(self):
        """Lista de vendas vazia deve retornar 0.0."""
        vendas = ()
        resultado = calcular_total_mensal(vendas)
        self.assertEqual(resultado, 0.0)

    def test_apenas_uma_venda(self):
        """Lista com apenas uma venda deve retornar exatamente seu valor."""
        vendas = ((1, 100.00),)
        resultado = calcular_total_mensal(vendas)
        self.assertAlmostEqual(resultado, 100.00, places=2)

    def test_vendas_com_valores_iguais(self):
        """Vendas com valores iguais de produtos diferentes."""
        vendas = ((1, 75.00), (2, 75.00), (3, 75.00))
        resultado = calcular_total_mensal(vendas)
        self.assertAlmostEqual(resultado, 225.00, places=2)


class TestCalcularVariacaoMensal(unittest.TestCase):
    """Testes para a função calcular_variacao_mensal(historico, mes).

    Recebe o histórico de vendas mensais e um mês de referência.
    Retorna o percentual de variação em relação ao mês anterior.
    Fórmula: ((valor_atual - valor_anterior) / valor_anterior) * 100
    """

    def test_variacao_positiva(self):
        """Mês com aumento de vendas retorna percentual positivo.

        '2/22': (1000.00 - 400.50) / 400.50 * 100 ≈ 149.69%.
        """
        historico = (
            ('1/22', 400.50),
            ('2/22', 1000.00),
            ('3/22', 10.50),
            ('4/22', 100.30),
        )
        resultado = calcular_variacao_mensal(historico, '2/22')
        self.assertAlmostEqual(resultado, 149.69, places=2)

    def test_variacao_negativa(self):
        """Mês com queda de vendas retorna percentual negativo.

        '3/22': (10.50 - 1000.00) / 1000.00 * 100 = -98.95%.
        """
        historico = (
            ('1/22', 400.50),
            ('2/22', 1000.00),
            ('3/22', 10.50),
            ('4/22', 100.30),
        )
        resultado = calcular_variacao_mensal(historico, '3/22')
        self.assertAlmostEqual(resultado, -98.95, places=2)

    def test_primeiro_mes_sem_mes_anterior(self):
        """Primeiro mês da lista não possui mês anterior: deve retornar None."""
        historico = (
            ('1/22', 400.50),
            ('2/22', 1000.00),
            ('3/22', 10.50),
            ('4/22', 100.30),
        )
        resultado = calcular_variacao_mensal(historico, '1/22')
        self.assertIsNone(resultado)

    def test_variacao_zero(self):
        """Meses consecutivos com mesmo valor resultam em variação zero."""
        historico = (('5/22', 500.00), ('6/22', 500.00))
        resultado = calcular_variacao_mensal(historico, '6/22')
        self.assertAlmostEqual(resultado, 0.0, places=2)


if __name__ == '__main__':
    unittest.main()
