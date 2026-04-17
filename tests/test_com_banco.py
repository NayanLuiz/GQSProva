import sqlite3
import unittest

from banco import (
    filtrar_produtos,
    listar_produtos_venda,
    listar_produtos_ordenados,
    listar_vendas_responsavel,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def criar_banco_teste():
    """Cria e popula um banco SQLite em memória para uso nos testes."""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE Usuario (
            id           INTEGER PRIMARY KEY,
            nome         TEXT    NOT NULL,
            endereco     TEXT,
            tipo_usuario TEXT
        );

        CREATE TABLE Produto (
            id         INTEGER PRIMARY KEY,
            nome       TEXT    NOT NULL,
            codigo     TEXT    UNIQUE,
            categoria  TEXT,
            preco      REAL,
            quantidade INTEGER
        );

        CREATE TABLE Venda (
            id             INTEGER PRIMARY KEY,
            id_responsavel INTEGER,
            total          REAL,
            FOREIGN KEY (id_responsavel) REFERENCES Usuario(id)
        );

        CREATE TABLE Produto_venda (
            id         INTEGER PRIMARY KEY,
            id_produto INTEGER,
            id_venda   INTEGER,
            quantidade INTEGER,
            FOREIGN KEY (id_produto) REFERENCES Produto(id),
            FOREIGN KEY (id_venda)   REFERENCES Venda(id)
        );
    ''')

    cursor.executemany('INSERT INTO Usuario VALUES (?, ?, ?, ?)', [
        (1, 'Ana Silva',   'Rua A, 123', 'gerente'),
        (2, 'Bruno Souza', 'Rua B, 456', 'vendedor'),
        (3, 'Carlos Lima', 'Rua C, 789', 'vendedor'),
    ])

    cursor.executemany('INSERT INTO Produto VALUES (?, ?, ?, ?, ?, ?)', [
        (1, 'Shampoo',       'SH001', 'Higiene',  12.90, 10),
        (2, 'Condicionador', 'CD001', 'Higiene',  15.90,  5),
        (3, 'Sabonete',      'SB001', 'Higiene',   3.50,  2),
        (4, 'Detergente',    'DT001', 'Limpeza',   2.50,  8),
        (5, 'Esponja',       'ES001', 'Limpeza',   1.50, 15),
    ])

    cursor.executemany('INSERT INTO Venda VALUES (?, ?, ?)', [
        (1, 1,  50.50),
        (2, 1, 200.95),
        (3, 2,  20.95),
    ])

    # Venda 1: Shampoo (id=1) e Condicionador (id=2)
    # Venda 2: Sabonete (id=3)
    # Venda 3: Detergente (id=4)
    cursor.executemany('INSERT INTO Produto_venda VALUES (?, ?, ?, ?)', [
        (1, 1, 1, 2),
        (2, 2, 1, 1),
        (3, 3, 2, 3),
        (4, 4, 3, 1),
    ])

    conn.commit()
    return conn


def criar_banco_somente_schema():
    """Cria banco SQLite em memória apenas com o schema (sem dados)."""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE Usuario (
            id INTEGER PRIMARY KEY, nome TEXT NOT NULL,
            endereco TEXT, tipo_usuario TEXT
        );
        CREATE TABLE Produto (
            id INTEGER PRIMARY KEY, nome TEXT NOT NULL,
            codigo TEXT UNIQUE, categoria TEXT, preco REAL, quantidade INTEGER
        );
        CREATE TABLE Venda (
            id INTEGER PRIMARY KEY, id_responsavel INTEGER, total REAL,
            FOREIGN KEY (id_responsavel) REFERENCES Usuario(id)
        );
        CREATE TABLE Produto_venda (
            id INTEGER PRIMARY KEY, id_produto INTEGER,
            id_venda INTEGER, quantidade INTEGER,
            FOREIGN KEY (id_produto) REFERENCES Produto(id),
            FOREIGN KEY (id_venda)   REFERENCES Venda(id)
        );
    ''')
    conn.commit()
    return conn


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

class TestFiltrarProdutos(unittest.TestCase):
    """Testes para a função filtrar_produtos(conn, nome, codigo, categoria).

    Filtra registros da tabela Produto por nome, código ou categoria.
    """

    def setUp(self):
        self.conn = criar_banco_teste()

    def tearDown(self):
        self.conn.close()

    def test_filtrar_por_nome(self):
        """Busca por nome existente deve retornar exatamente um produto."""
        resultado = filtrar_produtos(self.conn, nome='Shampoo')
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0][1], 'Shampoo')

    def test_filtrar_por_codigo(self):
        """Busca por código existente deve retornar exatamente um produto."""
        resultado = filtrar_produtos(self.conn, codigo='DT001')
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0][2], 'DT001')

    def test_filtrar_por_categoria(self):
        """Busca por categoria deve retornar todos os produtos daquela categoria."""
        resultado = filtrar_produtos(self.conn, categoria='Higiene')
        self.assertEqual(len(resultado), 3)
        for produto in resultado:
            self.assertEqual(produto[3], 'Higiene')

    def test_filtrar_por_categoria_inexistente(self):
        """Busca por categoria inexistente deve retornar lista vazia."""
        resultado = filtrar_produtos(self.conn, categoria='Beleza')
        self.assertEqual(len(resultado), 0)


class TestListarProdutosVenda(unittest.TestCase):
    """Testes para a função listar_produtos_venda(conn, id_venda).

    Retorna os nomes dos produtos de uma venda específica.
    """

    def setUp(self):
        self.conn = criar_banco_teste()

    def tearDown(self):
        self.conn.close()

    def test_venda_com_multiplos_produtos(self):
        """Venda existente com dois produtos retorna ambos os nomes."""
        resultado = listar_produtos_venda(self.conn, 1)
        nomes = [r[0] for r in resultado]
        self.assertEqual(len(resultado), 2)
        self.assertIn('Shampoo', nomes)
        self.assertIn('Condicionador', nomes)

    def test_venda_inexistente(self):
        """id_venda inexistente deve retornar lista vazia."""
        resultado = listar_produtos_venda(self.conn, 999)
        self.assertEqual(len(resultado), 0)

    def test_venda_com_apenas_um_produto(self):
        """Venda com um único produto retorna lista com exatamente um item."""
        resultado = listar_produtos_venda(self.conn, 3)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0][0], 'Detergente')


class TestListarProdutosOrdenados(unittest.TestCase):
    """Testes para a função listar_produtos_ordenados(conn).

    Retorna todos os produtos ordenados por categoria e depois por nome.
    """

    def setUp(self):
        self.conn = criar_banco_teste()

    def tearDown(self):
        self.conn.close()

    def test_ordenacao_por_categoria_e_nome(self):
        """Produtos são retornados com categorias em ordem crescente."""
        resultado = listar_produtos_ordenados(self.conn)
        self.assertGreater(len(resultado), 0)
        categorias = [r[3] for r in resultado]
        self.assertEqual(categorias, sorted(categorias))

    def test_banco_sem_produtos(self):
        """Tabela Produto vazia deve resultar em lista vazia."""
        conn_vazio = criar_banco_somente_schema()
        resultado = listar_produtos_ordenados(conn_vazio)
        self.assertEqual(len(resultado), 0)
        conn_vazio.close()

    def test_produtos_mesma_categoria_ordenados_por_nome(self):
        """Dentro da mesma categoria os produtos devem estar em ordem alfabética."""
        resultado = listar_produtos_ordenados(self.conn)
        higiene = [r for r in resultado if r[3] == 'Higiene']
        nomes = [r[1] for r in higiene]
        self.assertEqual(nomes, sorted(nomes))

    def test_apenas_uma_categoria(self):
        """Quando só existem produtos de uma categoria, retorna todos em ordem de nome."""
        conn_uma_cat = criar_banco_somente_schema()
        cursor = conn_uma_cat.cursor()
        cursor.executemany('INSERT INTO Produto VALUES (?, ?, ?, ?, ?, ?)', [
            (1, 'Shampoo',       'SH001', 'Higiene', 12.90, 10),
            (2, 'Condicionador', 'CD001', 'Higiene', 15.90,  5),
            (3, 'Sabonete',      'SB001', 'Higiene',  3.50,  2),
        ])
        conn_uma_cat.commit()
        resultado = listar_produtos_ordenados(conn_uma_cat)
        self.assertEqual(len(resultado), 3)
        nomes = [r[1] for r in resultado]
        self.assertEqual(nomes, sorted(nomes))
        # Nenhum produto da categoria 'Limpeza' aparece
        categorias = [r[3] for r in resultado]
        self.assertNotIn('Limpeza', categorias)
        conn_uma_cat.close()

    def test_entrada_parcial_nome(self):
        """Busca parcial com 'sh' via filtrar_produtos deve retornar Shampoo."""
        resultado = filtrar_produtos(self.conn, nome='sh')
        self.assertGreater(len(resultado), 0)
        nomes = [r[1] for r in resultado]
        self.assertIn('Shampoo', nomes)


class TestListarVendasResponsavel(unittest.TestCase):
    """Testes para a função listar_vendas_responsavel(conn, nome_responsavel).

    Retorna os ids das vendas associadas ao responsável informado.
    """

    def setUp(self):
        self.conn = criar_banco_teste()

    def tearDown(self):
        self.conn.close()

    def test_responsavel_com_multiplas_vendas(self):
        """Responsável com duas vendas deve retornar ambos os ids."""
        resultado = listar_vendas_responsavel(self.conn, 'Ana Silva')
        ids = [r[0] for r in resultado]
        self.assertEqual(len(resultado), 2)
        self.assertIn(1, ids)
        self.assertIn(2, ids)

    def test_responsavel_inexistente(self):
        """Nome não cadastrado deve retornar lista vazia."""
        resultado = listar_vendas_responsavel(self.conn, 'Pessoa Inexistente')
        self.assertEqual(len(resultado), 0)

    def test_responsavel_com_apenas_uma_venda(self):
        """Responsável com uma única venda deve retornar lista com um item."""
        resultado = listar_vendas_responsavel(self.conn, 'Bruno Souza')
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0][0], 3)

    def test_entrada_parcial_nome_responsavel(self):
        """Busca parcial por 'ana' retorna vendas de todos cujo nome contém 'ana'."""
        # Adiciona usuários e vendas extras para este cenário
        cursor = self.conn.cursor()
        cursor.executemany('INSERT INTO Usuario VALUES (?, ?, ?, ?)', [
            (4, 'Ana Clara',         'Rua D, 100', 'vendedor'),
            (5, 'Juliana Ferreira',  'Rua E, 200', 'vendedor'),
        ])
        cursor.executemany('INSERT INTO Venda VALUES (?, ?, ?)', [
            (4, 4, 80.00),
            (5, 5, 55.00),
        ])
        self.conn.commit()

        resultado = listar_vendas_responsavel(self.conn, 'ana')
        ids = [r[0] for r in resultado]
        # Deve incluir vendas de Ana Silva (1,2), Ana Clara (4) e Juliana (5)
        self.assertIn(1, ids)
        self.assertIn(2, ids)
        self.assertIn(4, ids)
        self.assertIn(5, ids)


if __name__ == '__main__':
    unittest.main()
