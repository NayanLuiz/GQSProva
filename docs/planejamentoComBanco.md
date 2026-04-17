# Planejamento – Testes com Banco de Dados

## Visão Geral

Sistema de controle de estoque e vendas desenvolvido em **Python** com **unittest** seguindo a metodologia **TDD**.  
Nesta etapa são criados os testes para as funcionalidades que **dependem do banco de dados**.

---

## Tecnologias

| Item | Escolha |
|------|---------|
| Linguagem | Python 3 |
| Framework de testes | unittest (biblioteca padrão) |
| Banco de dados (produção) | A definir (ex.: SQLite, PostgreSQL, MySQL) |
| Banco de dados (testes) | **SQLite em memória** (`sqlite3.connect(':memory:')`) |
| Metodologia | TDD — testes primeiro, implementação depois |

---

## Esquema do Banco de Dados

```sql
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
    id              INTEGER PRIMARY KEY,
    id_responsavel  INTEGER,
    total           REAL,
    FOREIGN KEY (id_responsavel) REFERENCES Usuario(id)
);

CREATE TABLE Produto_venda (
    id          INTEGER PRIMARY KEY,
    id_produto  INTEGER,
    id_venda    INTEGER,
    quantidade  INTEGER,
    FOREIGN KEY (id_produto) REFERENCES Produto(id),
    FOREIGN KEY (id_venda)   REFERENCES Venda(id)
);
```

---

## Dados de Teste (Fixture)

Para cada teste, um banco SQLite em memória é criado no `setUp` e destruído no `tearDown`, garantindo isolamento total entre os testes.

**Dados pré-populados:**

```
Usuario : (1,'Ana Silva','Rua A, 123','gerente'), (2,'Bruno Souza','Rua B, 456','vendedor'), (3,'Carlos Lima','Rua C, 789','vendedor')
Produto : (1,'Shampoo','SH001','Higiene',12.90,10), (2,'Condicionador','CD001','Higiene',15.90,5),
          (3,'Sabonete','SB001','Higiene',3.50,2), (4,'Detergente','DT001','Limpeza',2.50,8),
          (5,'Esponja','ES001','Limpeza',1.50,15)
Venda   : (1,1,50.50), (2,1,200.95), (3,2,20.95)
Produto_venda : (1,1,1,2), (2,2,1,1), (3,3,2,3), (4,4,3,1)
```

---

## Estrutura de Arquivos

```
tests/
└── test_com_banco.py   # testes com banco de dados

banco.py                # módulo de acesso ao banco (a implementar)
```

---

## Funções a Implementar

### 1. `filtrar_produtos(conn, nome=None, codigo=None, categoria=None)`

**Módulo:** `banco`

**Descrição:** Filtra produtos da tabela `Produto` por um ou mais critérios opcionais: nome, código ou categoria. Retorna uma lista de tuplas com todos os campos do produto.

**Assinatura esperada:**
```python
def filtrar_produtos(conn, nome=None, codigo=None, categoria=None) -> list:
    ...
```

**Exemplo:**
```python
filtrar_produtos(conn, nome='Shampoo')
# → [(1, 'Shampoo', 'SH001', 'Higiene', 12.90, 10)]

filtrar_produtos(conn, categoria='Limpeza')
# → [(4,'Detergente','DT001','Limpeza',2.50,8), (5,'Esponja','ES001','Limpeza',1.50,15)]
```

#### Casos de Teste

| # | Cenário | Parâmetro | Saída Esperada |
|---|---------|-----------|----------------|
| 1 | Filtro por nome existente | `nome='Shampoo'` | Lista com 1 produto cujo nome é 'Shampoo' |
| 2 | Filtro por código existente | `codigo='DT001'` | Lista com 1 produto cujo código é 'DT001' |
| 3 | Filtro por categoria existente | `categoria='Higiene'` | Lista com 3 produtos da categoria 'Higiene' |

---

### 2. `listar_produtos_venda(conn, id_venda)`

**Módulo:** `banco`

**Descrição:** Recebe o `id` de uma venda e retorna a lista dos **nomes** dos produtos que fazem parte daquela venda, consultando as tabelas `Produto_venda` e `Produto`.

**Assinatura esperada:**
```python
def listar_produtos_venda(conn, id_venda: int) -> list:
    ...
```

**Exemplo:**
```python
listar_produtos_venda(conn, 1)
# → [('Shampoo',), ('Condicionador',)]
```

#### Casos de Teste

| # | Cenário | `id_venda` | Saída Esperada |
|---|---------|-----------|----------------|
| 1 | Venda existente com múltiplos produtos | `1` | Lista com 'Shampoo' e 'Condicionador' (2 itens) |
| 2 | `id_venda` inexistente no banco | `999` | Lista vazia `[]` |
| 3 | Venda existente com apenas um produto | `3` | Lista com 1 item: 'Detergente' |

---

### 3. `listar_produtos_ordenados(conn)`

**Módulo:** `banco`

**Descrição:** Retorna todos os produtos da tabela `Produto`, ordenados primeiro por **categoria** (ascendente) e depois por **nome** (ascendente).

**Assinatura esperada:**
```python
def listar_produtos_ordenados(conn) -> list:
    ...
```

**Exemplo:**
```python
listar_produtos_ordenados(conn)
# → [...produtos da categoria 'Higiene' em ordem alfabética de nome...,
#    ...produtos da categoria 'Limpeza' em ordem alfabética de nome...]
```

#### Casos de Teste

| # | Cenário | Descrição | Verificação |
|---|---------|-----------|-------------|
| 1 | Banco com produtos de categorias diferentes | Ordenação normal | A lista de categorias retornada está em ordem crescente |
| 2 | Banco sem produtos (tabela vazia) | Sem registros | Retorna lista vazia `[]` |
| 3 | Produtos da mesma categoria | Só 'Higiene' na tabela | Nomes dentro da categoria estão em ordem alfabética crescente |

---

### 4. `listar_vendas_responsavel(conn, nome_responsavel)`

**Módulo:** `banco`

**Descrição:** Recebe o **nome** de um responsável (usuário) e retorna a lista dos **ids das vendas** em que ele foi responsável, consultando as tabelas `Venda` e `Usuario`.

**Assinatura esperada:**
```python
def listar_vendas_responsavel(conn, nome_responsavel: str) -> list:
    ...
```

**Exemplo:**
```python
listar_vendas_responsavel(conn, 'Ana Silva')
# → [(1,), (2,)]
```

#### Casos de Teste

| # | Cenário | `nome_responsavel` | Saída Esperada |
|---|---------|-------------------|----------------|
| 1 | Responsável com múltiplas vendas | `'Ana Silva'` | Lista com ids 1 e 2 (2 itens) |
| 2 | Nome não cadastrado no banco | `'Pessoa Inexistente'` | Lista vazia `[]` |
| 3 | Responsável com apenas uma venda | `'Bruno Souza'` | Lista com id 3 (1 item) |

---

## Arquivo de Testes

O arquivo de testes correspondente é:

```
tests/test_com_banco.py
```

Ele contém as classes:
- `TestFiltrarProdutos`
- `TestListarProdutosVenda`
- `TestListarProdutosOrdenados`
- `TestListarVendasResponsavel`

Cada classe possui `setUp` / `tearDown` para criação e destruição do banco em memória, e **3 métodos de teste**, conforme descrito acima.
