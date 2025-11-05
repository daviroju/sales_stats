#%%
import pandas as pd
import re
import plotly.express as px
from data import sp

# %%
def desempenho_equipe():
    sp_won = sp[sp['deal_stage'] == 'Won']
    sp_deal_stats = sp.groupby(['deal_stage', 'engage_date_my'], as_index=False).count()

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

    return total_sp
# %%
def figure_desempenho_equipe(df):
    media_geral = df['receita_vendas'].mean()
    fig = px.bar(
        df.sort_values(by='receita_vendas', ascending=False), 
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
    return fig

# %%
def desempenho_regional(df):
    total_sp_regional = df.groupby('regional_office', as_index=False)['receita_vendas'].sum()
    total_sp_regional['percentual_venda'] = total_sp_regional['receita_vendas'] / total_sp_regional['receita_vendas'].sum() * 100
    total_sp_regional = total_sp_regional.sort_values(by='percentual_venda', ascending=False)
    return total_sp_regional

def desempenho_equipe_regional(df):
    sp_agent:pd.DataFrame = df.groupby(['sales_agent', 'manager', 'regional_office'], as_index=False)['close_value'].sum().sort_values('close_value', ascending=False)
    sp_agent = sp_agent.reset_index(drop=True)
    return sp_agent

def desempenho_trimestral(df):
    TRIMESTRE = 'trimestre_close'
    sp_agent_month:pd.DataFrame = df.groupby([TRIMESTRE], as_index=False)['close_value'].sum().sort_values('close_value', ascending=False)
    sp_agent_month = sp_agent_month.reset_index(drop=True)
    return sp_agent_month


def figure_desempenho_trimestral(df):
    TRIMESTRE = 'trimestre_close'
    labels = {TRIMESTRE:'Trimestre', 'close_value':'Receita em R$'}
    fig = px.bar(
        df.sort_values(by=TRIMESTRE), 
        x=TRIMESTRE, 
        y="close_value", 
        color = 'trimestre_close',
        labels=labels)
    fig.update_traces(
        texttemplate="%{value:$,s}",
        textposition='outside'
    )   
    return fig


def desempenho_produto_receita(df):
    total_tentativas_por_produto = sp.groupby('Produto', as_index=False)['opportunity_id'].count().rename(columns={'opportunity_id': 'total_tentativas'})
    vendas_won_por_produto = df.groupby('Produto', as_index=False).agg(
        receita_total=('close_value', 'sum'),
        vendas_won=('opportunity_id', 'count')
    )

    produto_maior_receita = pd.merge(vendas_won_por_produto, total_tentativas_por_produto, on='Produto')
    produto_maior_receita['taxa_sucesso'] = (produto_maior_receita['vendas_won'] / produto_maior_receita['total_tentativas'] * 100).round(2)
    produto_maior_receita = produto_maior_receita.sort_values('receita_total', ascending=False)
    produto_maior_receita = produto_maior_receita.rename(columns={'receita_total': 'close_value'})

    return produto_maior_receita[['Produto', 'close_value', 'vendas_won', 'total_tentativas', 'taxa_sucesso']]


def desempenho_produto_regional(df):
    produto_regional_top = (
        df
        .groupby(['regional_office', 'Produto'], as_index=False)['opportunity_id'].count()
        .rename(columns={'opportunity_id': 'qtd_vendas'})
    )
    produto_regional_top = (
        produto_regional_top.loc[
            produto_regional_top.groupby('regional_office')['qtd_vendas'].idxmax()
        ]
    )
    return produto_regional_top

#%%
df_won = sp[sp['deal_stage'] == 'Won']
df_desempenho_equipe = desempenho_equipe()
print(df_desempenho_equipe.reset_index(drop=True))
figure_desempenho_eq = figure_desempenho_equipe(df_desempenho_equipe)


#%%
df_desempenho_regional = desempenho_regional(df_desempenho_equipe)
print(df_desempenho_regional.reset_index(drop=True))

#%%
df_desempenho_agente = desempenho_equipe_regional(df_won)
print(df_desempenho_agente)

#%%
df_trimestral = desempenho_trimestral(df_won)
figure_trimestral = figure_desempenho_trimestral(df_trimestral)

#%%
produto_mais_vendido_por_regional = desempenho_produto_regional(df_won).sort_values('qtd_vendas', ascending=False)
print(produto_mais_vendido_por_regional.reset_index(drop=True))
print('\n')

#%%
desempenho_vendas_por_produto = desempenho_produto_receita(df_won).reset_index(drop=True)
print(desempenho_vendas_por_produto)

# %%

figure_trimestral.show()
figure_trimestral.write_image("figures/receita_trimestral.png", width=1200, height=800)
figure_desempenho_eq.show()
figure_desempenho_eq.write_image("figures/vendas_gerentes.png", width=1200, height=800)