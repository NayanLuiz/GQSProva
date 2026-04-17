# Planejamento – Testes sem Banco de Dados

## Visão Geral

Sistema de controle de estoque e vendas desenvolvido em **Python** com **unittest** seguindo a metodologia **TDD** (Test-Driven Development).  
Nesta etapa são criados os testes para as funcionalidades que **não dependem de banco de dados**.

---

## Tecnologias

| Item | Escolha |
|------|---------|
| Linguagem | Python 3 |
| Framework de testes | unittest (biblioteca padrão) |
| Metodologia | TDD — testes primeiro, implementação depois |

---

## Estrutura de Arquivos

```
tests/
└── test_sem_banco.py   # testes sem banco de dados

estoque.py              # módulo de estoque (a implementar)
vendas.py               # módulo de vendas  (a implementar)
```

---

## Funções a Implementar

### 1. `verificar_reposicao(produtos)`

**Módulo:** `estoque`

**Descrição:** Recebe uma lista de tuplas `(nome, quantidade)` e retorna a quantidade de produtos que precisam de reposição, ou seja, aqueles cuja `quantidade < 5`.

**Assinatura esperada:**
```python
def verificar_reposicao(produtos: tuple) -> int:
    ...
```

**Exemplo:**
```python
entrada: (('Shampoo', 10), ('Condicionador', 5), ('Sabonete', 2))
saída:   1   # apenas 'Sabonete' tem quantidade < 5
```

#### Casos de Teste

| # | Cenário | Entrada | Saída Esperada |
|---|---------|---------|----------------|
| 1 | Lista com mix de quantidades (caso normal) | `(('Shampoo', 10), ('Condicionador', 5), ('Sabonete', 2))` | `1` |
| 2 | Lista vazia | `()` | `0` |
| 3 | Todos os produtos com quantidade ≥ 5 (nenhum precisa reposição) | `(('Shampoo', 10), ('Condicionador', 7), ('Sabonete', 5))` | `0` |

> **Nota:** Quantidade exatamente igual a 5 **não** dispara reposição (condição é `< 5`, não `<= 5`).

---

### 2. `calcular_percentual_vendas(vendas, produtos_ids)`

**Módulo:** `vendas`

**Descrição:** Recebe uma lista de tuplas `(id_venda, id_produto, quantidade)` e uma lista com todos os `id_produto` existentes, retornando o percentual de vendas de cada produto em relação ao total de unidades vendidas.

**Assinatura esperada:**
```python
def calcular_percentual_vendas(vendas: tuple, produtos_ids: list) -> list:
    ...
```

**Exemplo:**
```python
vendas      = ((1, 1, 4), (1, 2, 3), (1, 3, 1), (2, 1, 3))
produtos_ids = [1, 2, 3, 4]
# Total unidades vendidas: 4+3+1+3 = 11
# Produto 1: 4 (venda 1) + 3 (venda 2) = 7 → 7/11 ≈ 0.6364
# Produto 2: 3 (venda 1)                    → 3/11 ≈ 0.2727
# Produto 3: 1 (venda 1)                    → 1/11 ≈ 0.0909
# Produto 4: sem vendas                     → 0/11 = 0.0000
saída: [(1, 0.6364), (2, 0.2727), (3, 0.0909), (4, 0.0)]
```

> **Observação:** O enunciado original menciona `0.6365` para o produto 1, mas o valor matematicamente correto com arredondamento padrão (4 casas decimais) é `0.6364`. Os testes usam `assertAlmostEqual` com tolerância de 4 casas decimais.

#### Casos de Teste

| # | Cenário | Entrada | Saída Esperada |
|---|---------|---------|----------------|
| 1 | Lista normal com produto sem vendas (produto 4) | vendas acima, ids `[1,2,3,4]` | `[(1,≈0.6364),(2,≈0.2727),(3,≈0.0909),(4,0.0)]` |
| 2 | Lista de vendas vazia — todos os produtos com 0% | `()`, ids `[1,2,3]` | `[(1,0.0),(2,0.0),(3,0.0)]` |
| 3 | Apenas um produto e uma venda — 100% de participação | `((1, 1, 5),)`, ids `[1]` | `[(1,1.0)]` |

---

### 3. `calcular_total_mensal(vendas)`

**Módulo:** `vendas`

**Descrição:** Recebe uma lista de tuplas `(id_venda, valor_total)` e retorna a soma dos valores de todas as vendas do mês.

**Assinatura esperada:**
```python
def calcular_total_mensal(vendas: tuple) -> float:
    ...
```

**Exemplo:**
```python
entrada: ((1, 50.50), (2, 200.95), (3, 20.95), (4, 100.40))
saída:   372.80
```

#### Casos de Teste

| # | Cenário | Entrada | Saída Esperada |
|---|---------|---------|----------------|
| 1 | Lista normal com múltiplas vendas | `((1,50.50),(2,200.95),(3,20.95),(4,100.40))` | `372.80` |
| 2 | Lista de vendas vazia | `()` | `0.0` |
| 3 | Apenas uma venda | `((1, 100.00),)` | `100.00` |

---

### 4. `calcular_variacao_mensal(historico, mes)`

**Módulo:** `vendas`

**Descrição:** Recebe um histórico de vendas mensais como lista de tuplas `(mes, valor_total)` e um mês de referência. Retorna o percentual de variação do mês informado em comparação com o mês imediatamente anterior.

**Assinatura esperada:**
```python
def calcular_variacao_mensal(historico: tuple, mes: str) -> float | None:
    ...
```

**Fórmula:**
```
variacao (%) = ((valor_mes_atual - valor_mes_anterior) / valor_mes_anterior) * 100
```

**Exemplo:**
```python
historico = (('1/22', 400.50), ('2/22', 1000.00), ('3/22', 10.50), ('4/22', 100.30))

mes='2/22' → (1000.00 - 400.50) / 400.50 * 100 ≈ 149.69%
mes='3/22' → (10.50 - 1000.00) / 1000.00 * 100 = -98.95%
mes='1/22' → não há mês anterior → retorna None
```

#### Casos de Teste

| # | Cenário | Parâmetro `mes` | Saída Esperada |
|---|---------|-----------------|----------------|
| 1 | Mês com aumento de vendas | `'2/22'` | `≈ 149.69` |
| 2 | Mês com queda de vendas | `'3/22'` | `≈ -98.95` |
| 3 | Primeiro mês da lista (sem mês anterior) | `'1/22'` | `None` |

---

## Arquivo de Testes

O arquivo de testes correspondente é:

```
tests/test_sem_banco.py
```

Ele contém as classes:
- `TestVerificarReposicao`
- `TestCalcularPercentualVendas`
- `TestCalcularTotalMensal`
- `TestCalcularVariacaoMensal`

Cada classe possui **3 métodos de teste**, conforme descrito acima.
