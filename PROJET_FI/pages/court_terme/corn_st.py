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

'''
Sommaire : 

1_Import_Données_+_Définition_Vriables
2_Nettoyage_Données
3_Titre_+_Image
4_Fusion_Tableaux+_Ajout_Indicateurs
5_Séléction_Période
6_Sidebar_Séléction_Commodite_&_Indicateur
7_Affichage_Streamlit

'''
#____________________________________________________________________________________________________________________________________________

#                                                   1_Import_Données_+_Définition_Variables
#____________________________________________________________________________________________________________________________________________

commodite = 'corn'
unique_id = 'st'
df_corn = pd.read_csv("df_corn.csv",index_col=None)
df_index = pd.read_csv("df_index.csv",index_col=None)

#____________________________________________________________________________________________________________________________________________

#                                                   2_Nettoyage_Données
#____________________________________________________________________________________________________________________________________________

df_corn = clean_df(df_corn,commodite)
df_index = clean_df(df_index,'index')
df_corn_2 = df_corn.copy()

#____________________________________________________________________________________________________________________________________________

#                                                   3_Titre_+_Image
#____________________________________________________________________________________________________________________________________________

picture = get_picture(commodite)
title = "Le maïs, un pilier des matières premières agricoles"
subtitle = "Analyse approfondie des tendances, performances et métriques clés du marché du maïs"
display_header(picture, title, subtitle)
display_bar(df_corn_2, commodite)
reverse_dataframe(df_corn)

#____________________________________________________________________________________________________________________________________________

#                                                   4_Fusion_Tableaux+_Ajout_Indicateurs
#____________________________________________________________________________________________________________________________________________

sub_df_corn = pd.concat([df_corn, df_index], axis =1)
sub_df_corn_ind = sub_df_corn.copy()
df_ind(sub_df_corn_ind, commodite)

#____________________________________________________________________________________________________________________________________________

#                                                   5_Séléction_Période
#____________________________________________________________________________________________________________________________________________

sub_df_corn_ind_filtered = sub_df_corn_ind.iloc[:13,:]

#____________________________________________________________________________________________________________________________________________

#                                                   6_Sidebar_Séléction_Commodite_&_Indicateur
#____________________________________________________________________________________________________________________________________________

selected_commodity = st.sidebar.radio("Sélectionnez les cours à afficher", 
                                    [ commodite, 'Index', 'Les deux'],
                                    index=2)

selected_indicators = st.sidebar.radio("Sélectionnez les indicateurs à afficher", 
                                    [ f'MM_{commodite}', f'RSI_{commodite}', f'Stochastic_{commodite}'])

#____________________________________________________________________________________________________________________________________________

#                                                   7_Affichage_Streamlit
#____________________________________________________________________________________________________________________________________________

display_custom_table(df_corn_2.iloc[:13,:], "Données descriptives sur le maïs")

# Générer les graphiques
fig1, title1 = graph_cours_boursier(sub_df_corn_ind_filtered, selected_commodity, commodite)
fig2 = graph_indicateurs(sub_df_corn_ind_filtered, commodite, selected_indicators)

# Appeler la fonction pour afficher les graphiques avec des titres sous chaque graphique
# Appel de la fonction display_graphs
display_graphs(
    fig1=fig1,
    title1="Graphique des cours boursiers",
    fig2=fig2,
    title2="Graphique des indicateurs techniques",
    text_column_content = """
           Attention : le réchauffement climatique, un enjeu de plus en plus préoccupant.            </p>
            <p style="text-align: justify;">
              Le réchauffement climatique joue un rôle clé dans la volatilité des prix agricoles, notamment pour le maïs. Les conditions météorologiques extrêmes, telles que les sécheresses ou les pluies excessives, perturbent les cycles de semis et de récolte, réduisant les rendements. Une offre plus incertaine ou diminuée face à une demande stable ou croissante entraîne des hausses de prix. Par ailleurs, les événements climatiques peuvent aussi entraîner des coûts supplémentaires pour les producteurs, comme l'irrigation ou des stratégies d'adaptation, qui se répercutent sur les prix finaux. Cette instabilité rend le marché plus imprévisible, attirant parfois la spéculation, ce qui accentue encore davantage les fluctuations des prix.
            </p>
"""
)

#____________________________________________________________________________________________________________________________________________
