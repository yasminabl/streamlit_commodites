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

commodite = 'coffee'
unique_id = 'st'
df_coffee = pd.read_csv("df_coffee.csv",index_col=None)
df_index = pd.read_csv("df_index.csv",index_col=None)

#____________________________________________________________________________________________________________________________________________

#                                                   2_Nettoyage_Données
#____________________________________________________________________________________________________________________________________________

df_coffee = clean_df(df_coffee,commodite)
df_index = clean_df(df_index,'index')
df_coffee_2 = df_coffee.copy()

#____________________________________________________________________________________________________________________________________________

#                                                   3_Titre_+_Image
#____________________________________________________________________________________________________________________________________________

picture = get_picture(commodite)
title = "Café : l’or brun sous la loupe des investisseurs"
subtitle = "Analyse approfondie des tendances, performances et métriques clés du marché du café"
display_header(picture, title, subtitle)
display_bar(df_coffee_2, commodite)
reverse_dataframe(df_coffee)

#____________________________________________________________________________________________________________________________________________

#                                                   4_Fusion_Tableaux+_Ajout_Indicateurs
#____________________________________________________________________________________________________________________________________________

sub_df_coffee = pd.concat([df_coffee, df_index], axis =1)
sub_df_coffee_ind = sub_df_coffee.copy()
df_ind(sub_df_coffee_ind, commodite)

#____________________________________________________________________________________________________________________________________________

#                                                   5_Séléction_Période
#____________________________________________________________________________________________________________________________________________

sub_df_coffee_ind_filtered = sub_df_coffee_ind.iloc[:13,:]

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

display_custom_table(df_coffee_2.iloc[:13,:], "Données descriptives sur le café")

# Générer les graphiques
fig1, title1 = graph_cours_boursier(sub_df_coffee_ind_filtered, selected_commodity, commodite)
fig2 = graph_indicateurs(sub_df_coffee_ind_filtered, commodite, selected_indicators)

# Appeler la fonction pour afficher les graphiques avec des titres sous chaque graphique
# Appel de la fonction display_graphs
display_graphs(
    fig1=fig1,
    title1="Graphique des cours boursiers",
    fig2=fig2,
    title2="Graphique des indicateurs techniques",
    text_column_content = """
           "Nous n'avons jamais vu une telle flambée des prix", déclarait en juillet Giuseppe Lavazza.
        </p>
        <p style="text-align: justify;">
            Votre café du matin va-t-il devenir un luxe ? Les cours atteignent des sommets sur le marché
            des matières premières, alors que les principaux pays producteurs sont frappés par les effets 
            du dérèglement climatique.
        </p>
"""
)

#____________________________________________________________________________________________________________________________________________
