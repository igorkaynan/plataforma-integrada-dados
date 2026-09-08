-- =====================================================
-- PLATAFORMA INTEGRADA DE DADOS
-- Consultas analíticas da camada Gold
-- =====================================================


-- 1. Clientes com maior receita

SELECT
    cliente_id,
    nome,
    cidade,
    total_compras,
    receita_total,
    ticket_medio,
    segmento
FROM cliente_360
ORDER BY receita_total DESC;


-- 2. Clientes VIP

SELECT
    cliente_id,
    nome,
    email,
    cidade,
    receita_total
FROM cliente_360
WHERE segmento = 'VIP'
ORDER BY receita_total DESC;


-- 3. Receita por cidade

SELECT
    cidade,
    COUNT(DISTINCT cliente_id) AS total_clientes,
    SUM(receita_total) AS receita_total,
    AVG(ticket_medio) AS ticket_medio
FROM cliente_360
GROUP BY cidade
ORDER BY receita_total DESC;


-- 4. Performance dos produtos

SELECT
    produto,
    unidades_vendidas,
    total_vendas,
    receita_total,
    clientes_unicos
FROM performance_produtos
ORDER BY receita_total DESC;


-- 5. Produto com maior receita

SELECT
    produto,
    receita_total
FROM performance_produtos
ORDER BY receita_total DESC
LIMIT 1;


-- 6. Receita por segmento

SELECT
    segmento,
    COUNT(DISTINCT cliente_id) AS clientes,
    SUM(receita_total) AS receita_total,
    AVG(ticket_medio) AS ticket_medio
FROM cliente_360
GROUP BY segmento
ORDER BY receita_total DESC;