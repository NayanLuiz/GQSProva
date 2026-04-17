def filtrar_produtos(conn, nome=None, codigo=None, categoria=None) -> list:
    """Filtra produtos da tabela Produto por nome, código ou categoria.

    Suporta correspondência parcial (LIKE) para todos os campos.

    Parâmetros:
        conn: conexão com o banco de dados.
        nome: nome (ou trecho) do produto.
        codigo: código (ou trecho) do produto.
        categoria: categoria (ou trecho) do produto.

    Retorna:
        list: lista de tuplas com todos os campos do produto.
    """
    query = "SELECT * FROM Produto WHERE 1=1"
    params = []

    if nome is not None:
        query += " AND nome LIKE ?"
        params.append(f"%{nome}%")

    if codigo is not None:
        query += " AND codigo LIKE ?"
        params.append(f"%{codigo}%")

    if categoria is not None:
        query += " AND categoria LIKE ?"
        params.append(f"%{categoria}%")

    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()


def listar_produtos_venda(conn, id_venda: int) -> list:
    """Retorna os nomes dos produtos de uma venda específica.

    Parâmetros:
        conn: conexão com o banco de dados.
        id_venda: id da venda.

    Retorna:
        list: lista de tuplas com o nome de cada produto da venda.
    """
    query = """
        SELECT p.nome
        FROM Produto_venda pv
        JOIN Produto p ON p.id = pv.id_produto
        WHERE pv.id_venda = ?
    """
    cursor = conn.cursor()
    cursor.execute(query, (id_venda,))
    return cursor.fetchall()


def listar_produtos_ordenados(conn) -> list:
    """Retorna todos os produtos ordenados por categoria e depois por nome.

    Parâmetros:
        conn: conexão com o banco de dados.

    Retorna:
        list: lista de tuplas com todos os campos do produto, ordenadas.
    """
    query = "SELECT * FROM Produto ORDER BY categoria ASC, nome ASC"
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def listar_vendas_responsavel(conn, nome_responsavel: str) -> list:
    """Retorna os ids das vendas associadas a um responsável.

    Suporta correspondência parcial (LIKE) para o nome do responsável.

    Parâmetros:
        conn: conexão com o banco de dados.
        nome_responsavel: nome (ou trecho) do responsável.

    Retorna:
        list: lista de tuplas com o id de cada venda.
    """
    query = """
        SELECT v.id
        FROM Venda v
        JOIN Usuario u ON u.id = v.id_responsavel
        WHERE u.nome LIKE ?
    """
    cursor = conn.cursor()
    cursor.execute(query, (f"%{nome_responsavel}%",))
    return cursor.fetchall()
