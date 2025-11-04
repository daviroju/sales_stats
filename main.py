#%%
import pandas as pd
import re
import plotly.express as px
#%%
# importando os datasets
data_dictionary = pd.read_csv('data/data_dictionary.csv', sep=';', encoding='latin')
contas = pd.read_csv('data/contas.csv', sep=';', encoding='latin')
sp = pd.read_csv('data/sales_pipeline.csv', sep=';', encoding='latin')
st = pd.read_csv('data/sales_teams.csv', sep=';', encoding='latin')

sp['close_value'] = sp[' close_value '] 
sp = sp.drop(' close_value ', axis=1)

def convert_values(x):
    x = str(x)
    x = "".join(re.findall(r'\d', x))

    if not x:
        return None
    
    return int(x) / 100

sp['close_value'] = sp['close_value'].apply(lambda x: convert_values(x))

sp = pd.merge(sp, st, on='sales_agent')

sp['engage_date'] = pd.to_datetime(sp['engage_date'], dayfirst=True)
sp['close_date'] = pd.to_datetime(sp['close_date'], dayfirst=True)

sp['engage_date_my'] = sp['engage_date'].dt.strftime('%m-%Y')
sp['close_date_my'] = sp['close_date'].dt.strftime('%m-%Y')

sp['engage_date_m'] = sp['engage_date'].dt.month
sp['close_date_m'] = sp['close_date'].dt.month

sp['engage_date_y'] = sp['engage_date'].dt.year
sp['close_date_y'] = sp['close_date'].dt.year

sp['days_to_close'] = sp['close_date'] - sp['engage_date']
sp['days_to_close'] = pd.to_numeric(sp['days_to_close'].dt.days, downcast='integer')

sp['trimestre_close'] = sp['close_date'].dt.quarter.astype(str) + '°'
sp['trimestre_engage'] = sp['engage_date'].dt.quarter.astype(str) + '°'



# %%


sp_won = sp[sp['deal_stage'] == 'Won']
sp_won.columns


#%%

total_sp = (
    sp_won.groupby(['manager', 'regional_office'], as_index=False).agg(
        receita_vendas=('close_value', 'sum'),
        qtd_vendas=('close_value', 'count'),
    )
)

total_sp['percentual_venda'] = (
    total_sp['receita_vendas'] /
    total_sp['receita_vendas'].sum() * 100
)
total_sp = total_sp.sort_values(by='percentual_venda', ascending=False)


print('Desempenho por equipe:')
print(total_sp)
print('\n')


media_geral = total_sp['receita_vendas'].mean()


fig = px.bar(
    total_sp.sort_values(by='receita_vendas', ascending=False), 
    x='manager', 
    y="receita_vendas", 
    color='regional_office',
    labels={
        'manager': 'Gerente de Vendas',
        'receita_vendas': 'Receita Total (R$)',
        'regional_office': 'Filial Regional',
        'percentual_venda': '% do Total'
    }
)
              
fig.add_hline(
    y=media_geral,
    line_dash="dash",
    line_color="red",
    annotation_text=f"Média Geral por Gerente: R$ {media_geral:,.0f}",
    annotation_position="top right"
)

fig.update_layout(yaxis_title='Receita (R$)', xaxis_title='Gerente')
fig.update_traces(
    texttemplate="%{value:$,s}",
    textposition='outside'
)
fig.show()


fig.write_image("figures/gerentes.png", width=1200, height=800)
#%%
print('Desempenho por regional:')
total_sp_regional = total_sp.groupby('regional_office', as_index=False)['receita_vendas'].sum()
total_sp_regional['percentual_venda'] = total_sp_regional['receita_vendas'] / total_sp_regional['receita_vendas'].sum() * 100
total_sp_regional = total_sp_regional.sort_values(by='percentual_venda', ascending=False)
print(total_sp_regional)
print('\n')


#%%
print('Desempenho por agente de vendas:')
sp_agent:pd.DataFrame = sp_won.groupby(['sales_agent', 'manager', 'regional_office'], as_index=False)['close_value'].sum().sort_values('close_value', ascending=False)
sp_agent = sp_agent.reset_index(drop=True)
print(sp_agent)
print('\n')

#%%

TRIMESTRE = 'trimestre_close'

print('Desempenho trimestral:')
sp_agent_month:pd.DataFrame = sp_won.groupby([TRIMESTRE], as_index=False)['close_value'].sum().sort_values('close_value', ascending=False)
sp_agent_month = sp_agent_month.reset_index(drop=True)
print(sp_agent_month)
print('\n')


# %%
labels = {TRIMESTRE:'Trimestre', 'close_value':'Receita em R$'}
fig = px.bar(
    sp_agent_month.sort_values(by=TRIMESTRE), 
    x=TRIMESTRE, 
    y="close_value", 
    color = 'trimestre_close',
    labels=labels)
fig.update_traces(
    texttemplate="%{value:$,s}",
    textposition='outside'
)

fig.show()
fig.write_image("figures/receita.png", width=1200, height=800)
# %%

sales_products = sp_won.groupby(['Produto', 'regional_office'], as_index=False).agg(
    receita_total=('close_value', 'sum'),
    unidades_vendidas=('opportunity_id', 'count'),
    regiao_de_maior_venda=('regional_office', 'count')
)

total_tentativas_por_produto = sp.groupby('Produto', as_index=False)['opportunity_id'].count().rename(columns={'opportunity_id': 'total_tentativas'})
vendas_won_por_produto = sp_won.groupby('Produto', as_index=False).agg(
    receita_total=('close_value', 'sum'),
    vendas_won=('opportunity_id', 'count')
)

produto_maior_receita = pd.merge(vendas_won_por_produto, total_tentativas_por_produto, on='Produto')
produto_maior_receita['taxa_sucesso'] = (produto_maior_receita['vendas_won'] / produto_maior_receita['total_tentativas'] * 100).round(2)
produto_maior_receita = produto_maior_receita.sort_values('receita_total', ascending=False)

produto_maior_receita = produto_maior_receita.rename(columns={'receita_total': 'close_value'})
print('\n')
print('Produtos mais vendidos:')
print(produto_maior_receita[['Produto', 'close_value', 'vendas_won', 'total_tentativas', 'taxa_sucesso']])


produto_regional_top = (
    sp_won
    .groupby(['regional_office', 'Produto'], as_index=False)['opportunity_id'].count()
    .rename(columns={'opportunity_id': 'qtd_vendas'})
)
produto_regional_top = (
    produto_regional_top.loc[
        produto_regional_top.groupby('regional_office')['qtd_vendas'].idxmax()
    ]
)
print('\n')
print('Produto mais vendido por região:')
print(produto_regional_top)


#%%