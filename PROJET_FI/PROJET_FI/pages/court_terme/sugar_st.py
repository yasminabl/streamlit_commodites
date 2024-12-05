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
unique_id = 'st'
df_sugar = pd.read_csv("df_sugar.csv",index_col=None)
df_index = pd.read_csv("df_index.csv",index_col=None)

#_______________________________________________Nettoyage des doonées________________________________________________

df_sugar = clean_df(df_sugar,commodite)
df_index = clean_df(df_index,'index')
df_sugar_2 = df_sugar.copy()

 #__________________________________________TITRE ET IMAGE___________________________________________________________

picture = get_picture(commodite)
title = "Sucre : une douceur cotée au prix fort"
subtitle = "Analyse approfondie des tendances, performances et métriques clés du marché du sucre"
display_header(picture, title, subtitle)
display_bar(df_sugar_2, commodite)
reverse_dataframe(df_sugar)

#_______________________________________________________Fusion_+_Indicateurs_______________________________________________


sub_df_sugar = pd.concat([df_sugar, df_index], axis =1)
sub_df_sugar_ind = sub_df_sugar.copy()
df_ind(sub_df_sugar_ind, commodite)

#_________________________________________________________Selection_periode____________________________________________

sub_df_sugar_ind_filtered = sub_df_sugar_ind.iloc[:13,:]

#____________________________________________Sidebar_selection_commodite_+_indicateur____________________________________________

selected_commodity = st.sidebar.radio("Sélectionnez les cours à afficher", 
                                    [ commodite, 'Index', 'Les deux'],
                                    index=2)

selected_indicators = st.sidebar.radio("Sélectionnez les indicateurs à afficher", 
                                    [ f'MM_{commodite}', f'RSI_{commodite}', f'Stochastic_{commodite}'])


#_____________________________________________________Affichage_streamlit_______________________________________________

display_custom_table(df_sugar, "Données descriptives sur le sucre")

# Générer les graphiques
fig1, title1 = graph_cours_boursier(sub_df_sugar_ind_filtered, selected_commodity, commodite)
fig2 = graph_indicateurs(sub_df_sugar_ind_filtered, commodite, selected_indicators)

# Appeler la fonction pour afficher les graphiques avec des titres sous chaque graphique
# Appel de la fonction display_graphs
display_graphs(
    fig1=fig1,
    title1="Graphique des cours boursiers",
    fig2=fig2,
    title2="Graphique des indicateurs techniques",
    text_column_content = """
La volatilité des prix du sucre est fortement influencée par les conditions météorologiques et les dynamiques du marché mondial. Les sécheresses prolongées ou les excès de pluie peuvent perturber les cycles de production de la canne à sucre et de la betterave, entraînant des baisses de rendement et une diminution de l'offre. Par ailleurs, la hausse des coûts liés à la logistique, l’énergie, et les intrants agricoles pèse également sur les prix. À cela s’ajoute une demande mondiale croissante, alimentée par l’industrie alimentaire et les biocarburants, qui accentue la pression sur le marché. Cette combinaison de facteurs crée une instabilité propice à la spéculation, renforçant ainsi les fluctuations des prix du sucre.              
  </p>

"""
)

#________________________________________________________________________________________