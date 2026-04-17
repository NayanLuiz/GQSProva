# Conversa – Requisitos do Sistema de Controle de Estoque e Vendas

## Contexto

Registro da conversa de levantamento de requisitos para o sistema de controle de estoque e vendas, desenvolvido em Python com unittest no formato TDD.

---

## Solicitação

> **Gere apenas o planejamento e grave o planejamento em um novo arquivo docs de um sistema de controle de estoque e vendas. É para ser feito na linguagem Python e unittest no formato TDD. Fazendo primeiro os arquivos de testes para depois iniciar as funcionalidades do sistema. Utilize todas as informações dada aqui para contexto também. O contexto é o que está aqui na conversa.**
>
> **Faça 3 possibilidades para cada teste, por exemplo se vier algum dado vazio, alguns dados iguais, se só vier um dado e alguma possibilidade de dado que não corresponde com outros.**
>
> **Como primeiramente é para realizar os arquivos de testes, esses são os testes a serem feitos com banco de dados que está abaixo. Grave o plano em docs/planejamentoSemBanco.**

---

## Funcionalidades do Sistema

### Testes sem Banco de Dados

**1.** Receber uma lista de produtos com suas quantidades
```
(('Shampoo', 10), ('Condicionador', 5), ('Sabonete', 2))
```
e retornar a quantidade de produtos que precisa de reposição (quantidade < 5) — nesse caso seria **1 produto** ('Sabonete').

**2.** Receber uma lista com os produtos de uma venda `(id_venda, id_produto, quantidade)`
```
((1, 1, 4), (1, 2, 3), (1, 3, 1), (2, 1, 3))
```
e retornar o % de venda de cada um dos produtos (quais produtos mais são vendidos, ou seja, se são vendidos 100 produtos no total e 5 produtos de id=1, ele tem 5% de percentual de venda). Deve retornar uma lista da seguinte forma:
```
((1, 0.6365), (2, 0.2727), (3, 0.0909), (4, 0))
```

**3.** Receber uma lista com as vendas `(id_venda, valor_total)`
```
((1, 50.50), (2, 200.95), (3, 20.95), (4, 100.40))
```
e retornar o valor total arrecadado naquele mês.

**4.** Receber uma lista com os valores total de venda mensal
```
(('1/22', 400.50), ('2/22', 1000.00), ('3/22', 10.50), ('4/22', 100.30))
```
e retornar o percentual de aumento ou diminuição de venda do mês passado como parâmetro, em comparação com o mês anterior. Por exemplo, se for passado como parâmetro `'2/22'`, o retorno será **149%**. Se for passado como parâmetro `'3/22'`, o retorno será **-98,95%**.

---

> **Como primeiramente é para realizar os arquivos de testes, esses são os testes a serem feitos com banco de dados que está abaixo. Grave o plano em docs/planejamentoComBanco.**

### Testes com Banco de Dados

**1.** Fazer o filtro para buscar produtos por nome, código ou categoria.

**2.** Listar todos os produtos (nome) de uma venda passando o id da venda como parâmetro.

**3.** Listar produtos ordenando-os por categoria, nome.

**4.** Listar as vendas (id) de um responsável, passando como parâmetro o nome do responsável.

---

## Banco de Dados

O banco de dados utilizado tanto para os testes quanto para o sistema em si será:

1. **Usuario:** `id` (PK), `nome`, `endereço`, `tipo_usuario`
2. **Produto:** `id` (PK), `nome`, `codigo`, `categoria`, `preco`, `quantidade`
3. **Venda:** `id` (PK), `id_responsavel` (FK), `total`
4. **Produto_venda:** `id` (PK), `id_produto` (FK), `id_venda` (FK), `quantidade`

---

> **Por fim, grave nossas conversas em docs/conversa.**
>
> **Qualquer dúvida me pergunte.**

---

## Atualização – Aumento da Quantidade de Testes

> **Atualize o docs/ para aumentar a quantidade de testes para cada caso.**

### Testes sem Banco de Dados

**Caso 1 (`verificar_reposicao`):**
> Coloque no planejamento a possibilidade de vir todos os produtos com a quantidade abaixo de 5 e mais um teste com alguma entrada inválida com mensagem "Dado inválido", por exemplo como uma quantidade negativa.

Novos casos adicionados ao planejamento:
- **Caso 4:** Todos os produtos com quantidade < 5 → retorna o total de produtos da lista.
- **Caso 5:** Entrada inválida (quantidade negativa) → lança exceção com mensagem `"Dado inválido"`.

---

**Caso 2 (`calcular_percentual_vendas`):**
> Coloque no planejamento a possibilidade de vir mais de um produto com a mesma quantidade de venda, logo mesmo percentual. Além disso, coloque também novos testes de vendas diferentes com a mesma quantidade vendida e vendas com o mesmo produto com quantidades diferentes.

Novos casos adicionados ao planejamento:
- **Caso 4:** Dois produtos com a mesma quantidade total vendida → ambos retornam o mesmo percentual (ex.: 50% cada).
- **Caso 5:** Vendas com ids distintos mas mesma quantidade vendida por produto → cada produto retorna percentual igual.
- **Caso 6:** Mesmo produto aparece em vendas distintas com quantidades diferentes → o total do produto é a soma de todas as ocorrências.

---

**Caso 3 (`calcular_total_mensal`):**
> Coloque no planejamento a possibilidade com os valores vendidos iguais de produtos diferentes.

Novo caso adicionado ao planejamento:
- **Caso 4:** Vendas com valores iguais de produtos diferentes → retorna a soma correta de todos os valores.

---

**Caso 4 (`calcular_variacao_mensal`):**
> Coloque no planejamento a possibilidade ter meses conseguintes com a mesma quantidade de venda, logo com a saída espera 0.0.

Novo caso adicionado ao planejamento:
- **Caso 4:** Dois meses consecutivos com o mesmo valor de venda → variação é `0.0`.

---

### Testes com Banco de Dados

**Caso 1 (`filtrar_produtos`):**
> Coloque no planejamento a possibilidade de filtrar por algo que não é uma categoria do dado.

Novo caso adicionado ao planejamento:
- **Caso 4:** Filtro por categoria inexistente nos dados (ex.: `categoria='Beleza'`) → retorna lista vazia.

---

**Caso 3 (`listar_produtos_ordenados`):**
> Coloque no planejamento a possibilidade de listar categoria sem itens, apenas uma categoria com todos os produtos, colocar também se será listado quando receber uma entrada parcial (sh = shampoo).

Novos casos adicionados ao planejamento:
- **Caso 4:** Banco populado com apenas uma categoria (somente 'Higiene') → todos os produtos retornam ordenados por nome; nenhum item de 'Limpeza' aparece.
- **Caso 5:** Busca por entrada parcial de nome do produto (ex.: `'sh'` → 'Shampoo') via `filtrar_produtos` com suporte a `LIKE '%sh%'`.

---

**Caso 4 (`listar_vendas_responsavel`):**
> Coloque no planejamento a possibilidade de listar quando receber uma entrada parcial (ana = ana clara, juliana).

Novo caso adicionado ao planejamento:
- **Caso 4:** Busca por entrada parcial do nome do responsável (ex.: `'ana'` → Ana Clara, Juliana) utilizando `LIKE '%ana%'`; o fixture deve incluir os usuários extras necessários.

---

> **Grave novamente a conversa em docs/conversa.**

