# GQSProva — Sistema de Controle de Estoque e Vendas

Sistema desenvolvido em **Python** com **unittest**, seguindo a metodologia **TDD** (Test-Driven Development).

---

## Tecnologias

| Item | Escolha |
|------|---------|
| Linguagem | Python 3 |
| Framework de testes | unittest (biblioteca padrão) |
| Banco de dados (testes) | SQLite em memória (`sqlite3.connect(':memory:')`) |
| Metodologia | TDD — testes primeiro, implementação depois |

---

## Estrutura do Projeto

```
GQSProva/
├── banco.py                    # funções de acesso ao banco de dados
├── estoque.py                  # função de verificação de reposição
├── vendas.py                   # funções de cálculo de vendas
├── docs/
│   ├── conversa.md             # registro das conversas de requisitos
│   ├── planejamentoComBanco.md # planejamento dos testes com banco
│   └── planejamentoSemBanco.md # planejamento dos testes sem banco
├── tests/
│   ├── test_com_banco.py       # 16 testes com banco de dados
│   └── test_sem_banco.py       # 19 testes sem banco de dados
└── README.md
```

---

## Banco de Dados

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

## Módulos Implementados

### `estoque.py`

| Função | Descrição |
|--------|-----------|
| `verificar_reposicao(produtos)` | Recebe uma tupla de `(nome, quantidade)` e retorna a quantidade de produtos com `quantidade < 5`. Lança `ValueError("Dado inválido")` para quantidades negativas. |

### `vendas.py`

| Função | Descrição |
|--------|-----------|
| `calcular_percentual_vendas(vendas, produtos_ids)` | Recebe vendas `(id_venda, id_produto, quantidade)` e uma lista de ids de produtos. Retorna lista de `(id_produto, percentual)` com o percentual de participação de cada produto no total vendido. |
| `calcular_total_mensal(vendas)` | Recebe vendas `(id_venda, valor_total)` e retorna a soma dos valores. |
| `calcular_variacao_mensal(historico, mes)` | Recebe histórico `(mes, valor_total)` e um mês de referência. Retorna o percentual de variação em relação ao mês anterior. Fórmula: `((atual - anterior) / anterior) * 100`. Retorna `None` se não houver mês anterior. |

### `banco.py`

| Função | Descrição |
|--------|-----------|
| `filtrar_produtos(conn, nome, codigo, categoria)` | Filtra produtos por nome, código ou categoria com suporte a correspondência parcial (`LIKE`). |
| `listar_produtos_venda(conn, id_venda)` | Retorna os nomes dos produtos de uma venda específica. |
| `listar_produtos_ordenados(conn)` | Retorna todos os produtos ordenados por categoria (ASC) e nome (ASC). |
| `listar_vendas_responsavel(conn, nome_responsavel)` | Retorna os ids das vendas de um responsável, com suporte a busca parcial (`LIKE`). |

---

## Testes

### Testes sem Banco de Dados (`tests/test_sem_banco.py`) — 19 testes

| Classe | Método | Cenário |
|--------|--------|---------|
| `TestVerificarReposicao` | `test_lista_com_produto_em_reposicao` | Lista mista: 1 produto com quantidade < 5 |
| | `test_lista_vazia` | Lista vazia → 0 |
| | `test_todos_com_quantidade_suficiente` | Todos com quantidade ≥ 5 → 0 |
| | `test_todos_precisam_reposicao` | Todos com quantidade < 5 → total da lista |
| | `test_entrada_invalida_quantidade_negativa` | Quantidade negativa → `ValueError` |
| `TestCalcularPercentualVendas` | `test_lista_normal_com_produto_sem_vendas` | 4 produtos, 1 sem vendas → 0.0 |
| | `test_lista_de_vendas_vazia` | Vendas vazia → todos 0.0 |
| | `test_apenas_um_produto_vendido` | 1 produto → 100% |
| | `test_dois_produtos_mesmo_percentual` | 2 produtos iguais → 50% cada |
| | `test_vendas_diferentes_mesma_quantidade` | 3 produtos iguais → ~33.33% cada |
| | `test_mesmo_produto_vendas_distintas` | Mesmo produto em vendas distintas → 100% |
| `TestCalcularTotalMensal` | `test_lista_normal_de_vendas` | Soma de múltiplas vendas |
| | `test_lista_de_vendas_vazia` | Vazia → 0.0 |
| | `test_apenas_uma_venda` | 1 venda → seu valor |
| | `test_vendas_com_valores_iguais` | 3 × R$75 = R$225 |
| `TestCalcularVariacaoMensal` | `test_variacao_positiva` | Aumento → ~149.69% |
| | `test_variacao_negativa` | Queda → ~-98.95% |
| | `test_primeiro_mes_sem_mes_anterior` | Sem anterior → `None` |
| | `test_variacao_zero` | Mesmo valor → 0.0% |

### Testes com Banco de Dados (`tests/test_com_banco.py`) — 16 testes

| Status | Classe | Método | Cenário |
|--------|--------|--------|---------|
| ✅ | `TestFiltrarProdutos` | `test_filtrar_por_nome` | Nome existente → 1 resultado |
| ✅ | | `test_filtrar_por_codigo` | Código existente → 1 resultado |
| ✅ | | `test_filtrar_por_categoria` | Categoria 'Higiene' → 3 resultados |
| ✅ | | `test_filtrar_por_categoria_inexistente` | Categoria 'Beleza' → lista vazia |
| ✅ | `TestListarProdutosVenda` | `test_venda_com_multiplos_produtos` | Venda 1 → Shampoo + Condicionador |
| ✅ | | `test_venda_inexistente` | id 999 → lista vazia |
| ✅ | | `test_venda_com_apenas_um_produto` | Venda 3 → Detergente |
| ✅ | `TestListarProdutosOrdenados` | `test_ordenacao_por_categoria_e_nome` | Categorias em ordem crescente |
| ✅ | | `test_banco_sem_produtos` | Tabela vazia → lista vazia |
| ✅ | | `test_produtos_mesma_categoria_ordenados_por_nome` | Nomes em ordem dentro de Higiene |
| ✅ | | `test_apenas_uma_categoria` | Só Higiene, sem Limpeza |
| ✅ | | `test_entrada_parcial_nome` | `nome='sh'` → Shampoo |
| ✅ | `TestListarVendasResponsavel` | `test_responsavel_com_multiplas_vendas` | Ana Silva → vendas 1 e 2 |
| ✅ | | `test_responsavel_inexistente` | Nome inexistente → lista vazia |
| ✅ | | `test_responsavel_com_apenas_uma_venda` | Bruno Souza → venda 3 |
| ✅ | | `test_entrada_parcial_nome_responsavel` | `'ana'` → vendas de Ana Silva, Ana Clara e Juliana |

---

## Como Executar os Testes

```bash
cd GQSProva
python -m unittest discover -s tests -v
```

**Último resultado (17/04/2026) — 35/35 ✅:**

```
Ran 35 tests in 0.022s

OK
```