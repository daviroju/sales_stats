#%%
import pandas as pd
import re
import plotly.express as px
#%%

data_dictionary = pd.read_csv('resources/data_dictionary.csv', sep=';', encoding='latin')
contas = pd.read_csv('resources/contas.csv', sep=';', encoding='latin')
sp = pd.read_csv('resources/sales_pipeline.csv', sep=';', encoding='latin')
st = pd.read_csv('resources/sales_teams.csv', sep=';', encoding='latin')

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

