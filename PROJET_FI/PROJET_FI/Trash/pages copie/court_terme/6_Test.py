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

df_wheat = pd.read_csv("df_wheat.csv", nrows=100,index_col=None)
df_corn = pd.read_csv("df_corn.csv", nrows=100,index_col=None)
df_coffee = pd.read_csv("df_coffee.csv", nrows=100,index_col=None)
df_index = pd.read_csv("df_index.csv", nrows=100,index_col=None)
df_sugar = pd.read_csv("df_sugar.csv", nrows=100,index_col=None)
df_coffee_2 = df_coffee.copy()


#_______________________________________________________________________________________________________________________
st.subheader("Données sur le café")
col1, col2 = st.columns([2, 3])
with col1 :
    st.subheader("Valeurs boursières quotidiennes du café")
    df_coffee = process_dataframe(df_coffee, 'coffee')
    df_coffee = drop_unnamed_columns(df_coffee)
    df_coffee_2 = process_dataframe(df_coffee_2, 'coffee')
    df_coffee_2 = drop_unnamed_columns(df_coffee_2)
    st.dataframe(df_coffee)


with col2 :
    st.subheader("Données descriptive sur le café")
    df_coffee_2.index = pd.to_datetime(df_coffee_2.index)
    df_coffee_2 = df_coffee_2.groupby(df_coffee_2.index.year).describe().T
    st.dataframe(df_coffee_2)

#_______________________________________________________________________________________________________________________
df_index = process_dataframe(df_index, 'index')
df_index = drop_unnamed_columns(df_index)

sub_df_coffee = pd.concat([df_coffee, df_index], axis =1)
sub_df_coffee_ind = sub_df_coffee.copy()

st.dataframe(sub_df_coffee)
#_______________________________________________________________________________________________________________________

sub_df_coffee_ind['MM_20'] = sub_df_coffee_ind['value_coffee'].rolling(window=20).mean()
sub_df_coffee_ind['MM_200'] = sub_df_coffee_ind['value_coffee'].rolling(window=200).mean()
sub_df_coffee_ind['RSI'] = compute_rsi(sub_df_coffee_ind['value_coffee'])
sub_df_coffee_ind['Stochastic'] = compute_stochastics(sub_df_coffee_ind['value_coffee'])
st.dataframe(sub_df_coffee_ind)

#_______________________________________________________________________________________________________________________


sub_df_coffee.index = pd.to_datetime(sub_df_coffee.index)
sub_df_coffee_ind.index = pd.to_datetime(sub_df_coffee.index)

years = sub_df_coffee.index.year.unique()
months = range(1, 13)  

selected_year_min = st.sidebar.selectbox("Sélectionnez l'année de départ", options=years)
selected_month_min = st.sidebar.selectbox("Sélectionnez le mois de départ", options=months)

selected_year_max = st.sidebar.selectbox("Sélectionnez l'année de fin", options=years)
selected_month_max = st.sidebar.selectbox("Sélectionnez le mois de fin", options=months)

start_date = pd.Timestamp(year=selected_year_min, month=selected_month_min, day=1)
end_date = pd.Timestamp(year=selected_year_max, month=selected_month_max, day=1) + pd.offsets.MonthEnd(1)


sub_df_coffee_filtered = sub_df_coffee[(sub_df_coffee.index >= pd.to_datetime(start_date)) & 
                            (sub_df_coffee.index <= pd.to_datetime(end_date))]

sub_df_coffee_ind_filtered = sub_df_coffee_ind[(sub_df_coffee.index >= pd.to_datetime(start_date)) & 
                            (sub_df_coffee_ind.index <= pd.to_datetime(end_date))]

#_______________________________________________________________________________________________________________________
commodities = ['value_coffee', 'value_index']
selected_commodities = st.sidebar.multiselect("Sélectionnez les commodités à afficher", commodities, default=commodities)

st.subheader("Graphique du café")
st.line_chart(sub_df_coffee_filtered [selected_commodities])
#_______________________________________________________________________________________________________________________

#_______________________________________________________________________________________________________________________

selected_indicators = st.sidebar.multiselect("Sélectionnez les indicateurs à afficher", 
                                      [ 'MM_20', 'MM_200', 'RSI', 'Stochastic'], 
                                      default=['MM_20', 'MM_200'])


# Création du graphique avec Plotly
fig = go.Figure()

# Ajout des traces pour les commodités sélectionnées
if 'MM_20' in selected_indicators:
    fig.add_trace(go.Scatter(x=sub_df_coffee_ind_filtered.index, y=sub_df_coffee_ind_filtered['MM_20'], mode='lines', name='MM 20'))
if 'MM_200' in selected_indicators:
    fig.add_trace(go.Scatter(x=sub_df_coffee_ind_filtered.index, y=sub_df_coffee_ind_filtered['MM_200'], mode='lines', name='MM 200'))
if 'RSI' in selected_indicators:
    fig.add_trace(go.Scatter(x=sub_df_coffee_ind_filtered.index, y=sub_df_coffee_ind_filtered['RSI'], mode='lines', name='RSI'))
if 'Stochastic' in selected_indicators:
    fig.add_trace(go.Scatter(x=sub_df_coffee_ind_filtered.index, y=sub_df_coffee_ind_filtered['Stochastic'], mode='lines', name='Stochastic'))

# Mise en forme du graphique
fig.update_layout(title="Graphique des indicateurs techniques",
                  xaxis_title="Date",
                  yaxis_title="Valeur",
                  legend_title="Indicateurs")

# Affichage du graphique dans Streamlit
st.plotly_chart(fig)
#_______________________________________________________________________________________________________________________
