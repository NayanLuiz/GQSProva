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
