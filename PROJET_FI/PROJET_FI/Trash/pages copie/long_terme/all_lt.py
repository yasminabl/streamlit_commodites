import requests #68S617QRYKZHX4ZN #I1TVUXGTKDYPXB78
import pandas as pd
import streamlit as st 
import plotly 
import numpy as np
import plotly.graph_objects as go
import altair as alt
import plotly.express as px
from datetime import datetime
from functions import *



df_wheat = pd.read_csv("df_wheat.csv", index_col=None)
df_corn = pd.read_csv("df_corn.csv", index_col=None)
df_coffee = pd.read_csv("df_coffee.csv", index_col=None)
df_index = pd.read_csv("df_index.csv", index_col=None)
df_sugar = pd.read_csv("df_sugar.csv", index_col=None)

#__________________________________________________ALL_long_terme_______________________________________________________
st.subheader("Données sur le café")
col1, col2 = st.columns([2, 3])
with col1 :
    st.subheader("Valeurs boursières quotidiennes du café")
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

    st.dataframe(df_coffee)
    st.dataframe(df_corn)
    st.dataframe(df_sugar)
    st.dataframe(df_wheat)
    st.dataframe(df_index)


df_main = pd.concat([df_coffee, df_sugar, df_corn, df_wheat, df_index], axis=1)
st.write('df_main')
st.write(df_main.index.dtype)
df_main = df_main.sort_index(ascending=False)
df_main.index = pd.to_datetime(df_main.index)
st.write('df_main_2')
st.write(df_main.index.dtype)


years = df_main.index.year.unique()
months = range(1, 13)  
last_month = df_main.index[-1].month 
current_month = df_main.index[0].month 

selected_year_min = st.sidebar.selectbox("Sélectionnez l'année de départ", options=years, index=len(years) - 1)
selected_month_min = st.sidebar.selectbox("Sélectionnez le mois de départ", options=months, index=list(months).index(last_month))

selected_year_max = st.sidebar.selectbox("Sélectionnez l'année de fin", options=years, index=0)
selected_month_max = st.sidebar.selectbox("Sélectionnez le mois de fin", options=months, index=list(months).index(current_month))

start_date = pd.Timestamp(year=selected_year_min, month=selected_month_min, day=1)
end_date = pd.Timestamp(year=selected_year_max, month=selected_month_max, day=1) + pd.offsets.MonthEnd(1)

st.dataframe(df_main)
with col2 :
    st.subheader("Données descriptive sur les commodités pour l'année en cours")
    st.dataframe(df_main.describe())

#_______________________________________________________________________________________________________________________
df_main_ind = df_main.copy()

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
st.write(df_main_ind.index.dtype)
st.dataframe(df_main_ind)

#_______________________________________________________________________________________________________________________


df_main_ind.index = pd.to_datetime(df_main.index)


df_main_filtered = df_main[(df_main.index >= pd.to_datetime(start_date)) & 
                            (df_main.index <= pd.to_datetime(end_date))]

df_main_ind_filtered = df_main_ind[(df_coffee.index >= pd.to_datetime(start_date)) & 
                            (df_main_ind.index <= pd.to_datetime(end_date))]

df_main_filtered.index = df_main_filtered.index.strftime('%Y-%m-%d')
df_main_ind_filtered.index = df_main_ind_filtered.index.strftime('%Y-%m-%d')
#_______________________________________________________________________________________________________________________

#_______________________________________________________________________________________________________________________
selected_commodities = st.sidebar.multiselect("Sélectionnez les indicateurs à afficher", 
                                    ['value_coffee','value_sugar','value_corn','value_wheat', 'value_index'], 
                                    default=['value_coffee','value_sugar','value_corn','value_wheat', 'value_index'])

selected_indicators = st.sidebar.multiselect("Sélectionnez les indicateurs à afficher", 
                                    ['MM_coffee','MM_sugar','MM_corn','MM_wheat','MM_index', 
                                    'RSI_coffee','RSI_sugar','RSI_corn', 'RSI_wheat','RSI_index',
                                    'Stochastic_coffee',  'Stochastic_sugar', 'Stochastic_corn', 'Stochastic_wheat', 'Stochastic_index'], 
                                    default=['MM_coffee','MM_sugar','MM_corn','MM_wheat','MM_index'])

#_______________________________________________________________________________________________________________________

fig = go.Figure()

# Ajout des traces pour les commodités sélectionnées
if 'value_coffee' in selected_commodities:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['value_coffee'], mode='lines', name='value_coffee'))
if 'MM_coffee' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['MM_20_coffee'], mode='lines', name='MM 20_coffee'))
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['MM_200_coffee'], mode='lines', name='MM 200_coffee'))
if 'RSI_coffee' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['RSI_coffee'], mode='lines', name='RSI_coffee'))
if 'Stochastic_coffee' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['Stochastic_coffee'], mode='lines', name='Stochastic_coffee'))

if 'value_sugar' in selected_commodities:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['value_sugar'], mode='lines', name='value_sugar'))
if 'MM_sugar' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['MM_20_sugar'], mode='lines', name='MM 20_sugar'))
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['MM_200_sugar'], mode='lines', name='MM 200_sugar'))
if 'RSI_sugar' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['RSI_sugar'], mode='lines', name='RSI_sugar'))
if 'Stochastic_sugar' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['Stochastic_sugar'], mode='lines', name='Stochastic_sugar'))

if 'value_corn' in selected_commodities:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['value_corn'], mode='lines', name='value_corn'))
if 'MM_corn' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['MM_20_corn'], mode='lines', name='MM 20_corn'))
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['MM_200_corn'], mode='lines', name='MM 200_corn'))
if 'RSI_corn' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['RSI_corn'], mode='lines', name='RSI_corn'))
if 'Stochastic_corn' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['Stochastic_corn'], mode='lines', name='Stochastic_corn'))

if 'value_wheat' in selected_commodities:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['value_wheat'], mode='lines', name='value_wheat'))
if 'MM_wheat' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['MM_20_wheat'], mode='lines', name='MM 20_wheat'))
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['MM_200_wheat'], mode='lines', name='MM 200_wheat'))
if 'RSI_wheat' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['RSI_wheat'], mode='lines', name='RSI_wheat'))
if 'Stochastic_wheat' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['Stochastic_wheat'], mode='lines', name='Stochastic_wheat'))

if 'value_index' in selected_commodities:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['value_index'], mode='lines', name='value_index'))
if 'MM_index' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['MM_20_index'], mode='lines', name='MM 20_index'))
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['MM_200_index'], mode='lines', name='MM 200_index'))
if 'RSI_index' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['RSI_index'], mode='lines', name='RSI_index'))
if 'Stochastic_index' in selected_indicators:
    fig.add_trace(go.Scatter(x=df_main_ind_filtered.index, y=df_main_ind_filtered['Stochastic_index'], mode='lines', name='Stochastic_index'))

#_______________________________________________________________________________________________________________________

fig.update_layout(title="Graphique des indicateurs techniques",
                xaxis_title="Date",
                yaxis_title="Valeur",
                legend_title="Indicateurs")

# Affichage du graphique dans Streamlit
st.plotly_chart(fig)
#_______________________________________________________________________________________________________________________
