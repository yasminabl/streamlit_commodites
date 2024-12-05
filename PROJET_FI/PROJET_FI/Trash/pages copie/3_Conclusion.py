
import requests #68S617QRYKZHX4ZN #I1TVUXGTKDYPXB78
import pandas as pd
import streamlit as st 
import plotly 
import numpy as np
import plotly.graph_objects as go
import altair as alt
import plotly.express as px
from datetime import datetime, timedelta
from functions import *
import os 

df_wheat = pd.read_csv("df_wheat.csv", index_col=None)
df_corn = pd.read_csv("df_corn.csv", index_col=None)
df_coffee = pd.read_csv("df_coffee.csv", index_col=None)
df_index = pd.read_csv("df_index.csv", index_col=None)
df_sugar = pd.read_csv("df_sugar.csv", index_col=None)

#_______________________________________________________________________________________________________________________

df_coffee = process_dataframe(df_coffee, 'coffee')
df_coffee = drop_unnamed_columns(df_coffee)
df_sugar = process_dataframe(df_sugar, 'sugar')
df_sugar = drop_unnamed_columns(df_sugar)
df_corn = process_dataframe(df_corn, 'corn')
df_corn = drop_unnamed_columns(df_corn)
df_wheat = process_dataframe(df_wheat, 'wheat')
df_wheat = drop_unnamed_columns(df_wheat)
df_index = process_dataframe(df_index, 'index')
df_index = drop_unnamed_columns(df_index)
df_coffee.index = pd.to_datetime(df_coffee.index)
df_sugar.index = pd.to_datetime(df_sugar.index)
df_corn.index = pd.to_datetime(df_corn.index)
df_wheat.index = pd.to_datetime(df_wheat.index)
df_index.index = pd.to_datetime(df_index.index)
#_______________________________________________________________________________________________________________________

df_main = pd.concat([df_coffee, df_sugar, df_corn, df_wheat, df_index], axis=1)
df_main = df_main.iloc[::-1]
df_main_ind = df_main.copy()

#_______________________________________________________________________________________________________________________

df_main_ind['MM_20_coffee'] = df_main_ind['value_coffee'].iloc[::-1].rolling(window=20).mean().iloc[::-1]
df_main_ind['MM_200_coffee'] = df_main_ind['value_coffee'].iloc[::-1].rolling(window=200).mean().iloc[::-1]
df_main_ind['RSI_coffee'] = compute_rsi(df_main_ind['value_coffee'])
df_main_ind['Stochastic_coffee'] = compute_stochastics(df_main_ind['value_coffee'])

df_main_ind['MM_20_sugar'] = df_main_ind['value_sugar'].iloc[::-1].rolling(window=20).mean().iloc[::-1]
df_main_ind['MM_200_sugar'] = df_main_ind['value_sugar'].iloc[::-1].rolling(window=200).mean().iloc[::-1]
df_main_ind['RSI_sugar'] = compute_rsi(df_main_ind['value_sugar'])
df_main_ind['Stochastic_sugar'] = compute_stochastics(df_main_ind['value_sugar'])

df_main_ind['MM_20_corn'] = df_main_ind['value_corn'].iloc[::-1].rolling(window=20).mean().iloc[::-1]
df_main_ind['MM_200_corn'] = df_main_ind['value_corn'].iloc[::-1].rolling(window=200).mean().iloc[::-1]
df_main_ind['RSI_corn'] = compute_rsi(df_main_ind['value_corn'])
df_main_ind['Stochastic_corn'] = compute_stochastics(df_main_ind['value_corn'])

df_main_ind['MM_20_wheat'] = df_main_ind['value_wheat'].iloc[::-1].rolling(window=20).mean().iloc[::-1]
df_main_ind['MM_200_wheat'] = df_main_ind['value_wheat'].iloc[::-1].rolling(window=200).mean().iloc[::-1]
df_main_ind['RSI_wheat'] = compute_rsi(df_main_ind['value_wheat'])
df_main_ind['Stochastic_wheat'] = compute_stochastics(df_main_ind['value_wheat'])

df_main_ind['MM_20_index'] = df_main_ind['value_index'].iloc[::-1].rolling(window=20).mean().iloc[::-1]
df_main_ind['MM_200_index'] = df_main_ind['value_index'].iloc[::-1].rolling(window=200).mean().iloc[::-1]
df_main_ind['RSI_index'] = compute_rsi(df_main_ind['value_index'])
df_main_ind['Stochastic_index'] = compute_stochastics(df_main_ind['value_index'])

st.write('df_main_ind')
st.dataframe(df_main_ind)

#_______________________________________________________________________________________________________________________
conclusion_df = pd.DataFrame(columns=['Café', 'Sucre', 'Maïs', 'Blé'], index=['Tendance', 'Pression', 'Prévision'])
if df_main_ind.loc(1,'MM_20_coffee') > df_main_ind.loc(1,'value_coffee') :
    conclusion_df.loc['tendance', 'Café'].value = 'Haussière'
else : 
    conclusion_df.loc['tendance', 'Café'].value = 'Baissière'

if df_main_ind.loc(1,'RSI_coffee') > 80 :
    conclusion_df.loc['Pression', 'Café'].value = 'Vente'
elif df_main_ind.loc(1,'RSI_coffee') < 80 and df_main_ind.loc(1,'RSI_coffee') > 20 : 
    conclusion_df.loc['Pression', 'Café'].value = 'Attente'
else :
    conclusion_df.loc['Pression', 'Café'].value = 'Attente'

    


st.dataframe(conclusion_df)
#_______________________________________________________________________________________________________________________



#_______________________________________________________________________________________________________________________

#_______________________________________________________________________________________________________________________

#_______________________________________________________________________________________________________________________

#_______________________________________________________________________________________________________________________

