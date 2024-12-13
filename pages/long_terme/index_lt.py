import requests #68S617QRYKZHX4ZN #I1TVUXGTKDYPXB78
import pandas as pd
import streamlit as st 
import plotly 
import numpy as np
import plotly.graph_objects as go
import altair as alt
import plotly.express as px
from datetime import datetime
from features.functions import *
from features.layout import *
from PIL import Image
import base64

#____________________________________________Import_données_+_variables __________________________________________________________

commodite = 'index'
unique_id = 'lt'
df_index = pd.read_csv("df_index.csv",index_col=None)

#_______________________________________________Nettoyage des doonées________________________________________________

df_index = process_dataframe(df_index, 'index')
df_index = drop_unnamed_columns(df_index)
df_index_2 = df_index.copy()

 #__________________________________________TITRE ET IMAGE___________________________________________________________

picture = get_picture(commodite)
title = "Café : l’or brun sous la loupe des investisseurs"
subtitle = "Analyse approfondie des tendances, performances et métriques clés du marché du café"
display_header(picture, title, subtitle)
reverse_dataframe(df_index)

#_______________________________________________________Fusion_+_Indicateurs_______________________________________________

sub_df_index_ind = df_index.copy()
df_ind(sub_df_index_ind, commodite)

#_________________________________________________________Selection_periode____________________________________________

sub_df_index_ind.index = pd.to_datetime(sub_df_index_ind.index)

selected_year_min, selected_month_min, selected_year_max, selected_month_max = get_date_range_from_sidebar(sub_df_index_ind)

sub_df_coffee_ind_filtered = filter_dataframe(sub_df_index_ind, 
                                              selected_year_min, selected_month_min, 
                                              selected_year_max, selected_month_max)

#____________________________________________Sidebar_selection_commodite_+_indicateur____________________________________________
  
selected_commodity = st.sidebar.radio("Sélectionnez les cours à afficher", 
                                    [ commodite],
                                    index=0)

selected_indicators = st.sidebar.radio("Sélectionnez les indicateurs à afficher", 
                                    [ f'MM_{commodite}', f'RSI_{commodite}', f'Stochastic_{commodite}'])

#_____________________________________________________Affichage_streamlit_______________________________________________



# Assurez-vous que l'index est bien de type datetime
df_index['Date'] = pd.to_datetime(df_index['Date'], errors='coerce')
df_index.set_index('Date', inplace=True)

# Vérifiez les colonnes disponibles
st.write("Colonnes disponibles :", df_index.columns)

# Sidebar pour sélectionner les indicateurs
selected_indicators = st.sidebar.multiselect(
    "Sélectionnez les indicateurs à afficher",
    df_index.columns,
    default=[df_index.columns[0]]  # Par défaut, le premier indicateur
)

# Graphique des cours boursiers
fig_cours = go.Figure()

for indicator in selected_indicators:
    if indicator in df_index.columns:
        fig_cours.add_trace(go.Scatter(
            x=df_index.index,
            y=df_index[indicator],
            mode="lines",
            name=indicator
        ))

fig_cours.update_layout(
    title="Graphique des cours boursiers",
    xaxis_title="Date",
    yaxis_title="Valeur",
    legend_title="Indicateurs",
    template="plotly_white"
)

# Graphique des indicateurs techniques
fig_indicators = go.Figure()

# Ajouter les indicateurs techniques si disponibles
if "RSI" in df_index.columns:
    fig_indicators.add_trace(go.Scatter(
        x=df_index.index,
        y=df_index["RSI"],
        mode="lines",
        name="RSI"
    ))

if "Stochastic" in df_index.columns:
    fig_indicators.add_trace(go.Scatter(
        x=df_index.index,
        y=df_index["Stochastic"],
        mode="lines",
        name="Stochastic"
    ))

fig_indicators.update_layout(
    title="Graphique des indicateurs techniques",
    xaxis_title="Date",
    yaxis_title="Valeur",
    legend_title="Indicateurs",
    template="plotly_white"
)

# Affichage côte à côte des graphiques
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_cours, use_container_width=True)

with col2:
    st.plotly_chart(fig_indicators, use_container_width=True)
