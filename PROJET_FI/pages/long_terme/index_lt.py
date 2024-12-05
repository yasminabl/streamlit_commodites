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

'''
Sommaire : 

1_Import_Données_+_Définition_Vriables
2_Nettoyage_Données
3_Titre_+_Image
4_Ajout_Indicateurs
5_Séléction_Période
6_Sidebar_Séléction_Commodite_&_Indicateur
7_Affichage_Streamlit

'''

#____________________________________________________________________________________________________________________________________________

#                                                   1_Import_Données_+_Définition_Vriables
#____________________________________________________________________________________________________________________________________________

commodite = 'index'
unique_id = 'lt'
df_index = pd.read_csv("df_index.csv",index_col=None)

#____________________________________________________________________________________________________________________________________________

#                                                   2_Nettoyage_Données
#____________________________________________________________________________________________________________________________________________

df_index = process_dataframe(df_index, 'index')
df_index = drop_unnamed_columns(df_index)
df_index_2 = df_index.copy()

#____________________________________________________________________________________________________________________________________________

#                                                   3_Titre_+_Image
#____________________________________________________________________________________________________________________________________________

picture = get_picture(commodite)
title = "L'Index : Le Thermomètre Global des Marchés"
subtitle = "Plongez dans les tendances et performances qui définissent l'équilibre des commodités."
display_header(picture, title, subtitle)

reverse_dataframe(df_index)

#____________________________________________________________________________________________________________________________________________

#                                                   4_Ajout_Indicateurs
#____________________________________________________________________________________________________________________________________________

sub_df_index_ind = df_index.copy()
df_ind(sub_df_index_ind, commodite)

#____________________________________________________________________________________________________________________________________________

#                                                   5_Séléction_Période
#____________________________________________________________________________________________________________________________________________

sub_df_index_ind.index = pd.to_datetime(sub_df_index_ind.index)

selected_year_min, selected_month_min, selected_year_max, selected_month_max = get_date_range_from_sidebar(sub_df_index_ind)

sub_df_index_ind_filtered = filter_dataframe(sub_df_index_ind, 
                                              selected_year_min, selected_month_min, 
                                              selected_year_max, selected_month_max)

#____________________________________________________________________________________________________________________________________________

#                                                   6_Sidebar_Séléction_Commodite_&_Indicateur
#____________________________________________________________________________________________________________________________________________
  
selected_commodity = st.sidebar.radio("Sélectionnez les cours à afficher", 
                                    [ commodite],
                                    index=0)

selected_indicators = st.sidebar.radio("Sélectionnez les indicateurs à afficher", 
                                    [ f'MM_{commodite}', f'RSI_{commodite}', f'Stochastic_{commodite}'])

#____________________________________________________________________________________________________________________________________________

#                                                   7_Affichage_Streamlit
#____________________________________________________________________________________________________________________________________________

display_custom_table(df_index, "Données descriptives sur l'indice des commodités")

fig1, title1 = graph_cours_boursier_long_term(sub_df_index_ind_filtered, selected_commodity, commodite)
fig2 = graph_indicateurs(sub_df_index_ind_filtered, commodite, selected_indicators)

display_graphs_long_term(
    fig1=fig1,
    title1="Graphique des cours à long terme",
    fig2=fig2,
    title2="Graphique des indicateurs techniques (long terme)",
    text_column_content="""
        <p style="text-align: justify;">
        Les graphiques ci-dessus montrent l'évolution à long terme des cours de l'indice des commodités et des indices associés. 
        Les perspectives à long terme permettent de comprendre les cycles économiques et d'adapter les stratégies d'investissement.
        </p>
        <p style="text-align: justify;">
        Les indicateurs techniques offrent un aperçu supplémentaire sur les tendances sous-jacentes et la volatilité à long terme.
        </p>
    """
)

#____________________________________________________________________________________________________________________________________________
