# Sales Stats - Análise de Desempenho de Vendas

Sistema de análise de dados de vendas desenvolvido para fornecer insights estratégicos sobre o desempenho comercial da organização.

## Funcionalidades

- **Análise por Equipe**: Desempenho comparativo entre gerentes e regionais
- **Métricas de Produto**: Taxa de sucesso e receita por linha de produto
- **Indicadores Temporais**: Tendências trimestrais de vendas
- **Visualizações Interativas**: Gráficos de desempenho e distribuição geográfica

## Estrutura de Dados

O sistema utiliza quatro fontes de dados principais:
- `sales_pipeline.csv`: Pipeline de vendas com oportunidades e fechamentos
- `sales_teams.csv`: Estrutura organizacional das equipes comerciais
- `contas.csv`: Base de clientes e prospects
- `data_dictionary.csv`: Documentação dos campos de dados

## Métricas Principais

### Desempenho Comercial
- Receita total por gerente e regional
- Participação percentual de cada equipe no resultado
- Comparativo com média geral da organização

### Análise de Produtos
- Receita por linha de produto
- Taxa de conversão (vendas efetivadas/tentativas totais)
- Distribuição regional dos produtos mais vendidos

### Indicadores Temporais
- Performance trimestral consolidada
- Tempo médio de fechamento por oportunidade (em atualização futura)

## Execução
Utilizando o gerenciador de pacotes uv:
```bash
uv run main.py
```

Os relatórios são gerados automaticamente, incluindo gráficos salvos em `figures/`.

## Requisitos

- Python 3.13+
- Pandas, Plotly, NumPy (ver `pyproject.toml` para versões completas)
