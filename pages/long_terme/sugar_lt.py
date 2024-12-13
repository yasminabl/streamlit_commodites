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
import os 


#____________________________________________Import_données_+_variables __________________________________________________________


commodite = 'sugar'
unique_id = 'lt'
df_sugar = pd.read_csv("df_sugar.csv",index_col=None)
df_index = pd.read_csv("df_index.csv",index_col=None)

#_______________________________________________Nettoyage des doonées________________________________________________

df_sugar = clean_df(df_sugar,commodite)
df_index = clean_df(df_index,'index')
df_sugar_2 = df_sugar.copy()

 #__________________________________________TITRE ET IMAGE___________________________________________________________

picture = get_picture(commodite)
title = "Café : l’or brun sous la loupe des investisseurs"
subtitle = "Analyse approfondie des tendances, performances et métriques clés du marché du café"
display_header(picture, title, subtitle)
reverse_dataframe(df_sugar)

#_______________________________________________________Fusion_+_Indicateurs_______________________________________________

sub_df_sugar = pd.concat([df_sugar, df_index], axis =1)
sub_df_sugar_ind = sub_df_sugar.copy()
df_ind(sub_df_sugar_ind, commodite)

#_________________________________________________________Selection_periode____________________________________________


sub_df_sugar_ind.index = pd.to_datetime(sub_df_sugar_ind.index)

selected_year_min, selected_month_min, selected_year_max, selected_month_max = get_date_range_from_sidebar(sub_df_sugar_ind)

sub_df_sugar_ind_filtered = filter_dataframe(sub_df_sugar_ind, 
                                              selected_year_min, selected_month_min, 
                                              selected_year_max, selected_month_max)

#____________________________________________Sidebar_selection_commodite_+_indicateur____________________________________________

selected_commodity = st.sidebar.radio("Sélectionnez les cours à afficher", 
                                    [ commodite, 'Index', 'Les deux'],
                                    index=2)

selected_indicators = st.sidebar.radio("Sélectionnez les indicateurs à afficher", 
                                    [ f'MM_{commodite}', f'RSI_{commodite}', f'Stochastic_{commodite}'])

#_____________________________________________________Affichage_streamlit_______________________________________________

# Display descriptive statistics for coffee
display_custom_table(df_sugar, "Données descriptives sur le sucre")

# ___________________________________________ Generate Graphs ___________________________________________

fig1, title1 = graph_cours_boursier_long_term(sub_df_sugar_ind_filtered, selected_commodity, commodite)
fig2 = graph_indicateurs(sub_df_sugar_ind_filtered, commodite, selected_indicators)

display_graphs_long_term(
    fig1=fig1,
    title1="Graphique des cours à long terme",
    fig2=fig2,
    title2="Graphique des indicateurs techniques (long terme)",
    text_column_content="""
        <p style="text-align: justify;">
        Les graphiques ci-dessus montrent l'évolution à long terme des cours du sucre et des indices associés. 
        Les perspectives à long terme permettent de comprendre les cycles économiques et d'adapter les stratégies d'investissement.
        </p>
        <p style="text-align: justify;">
        Les indicateurs techniques offrent un aperçu supplémentaire sur les tendances sous-jacentes et la volatilité à long terme.
        </p>
    """
)