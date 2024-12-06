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

commodite = 'wheat'
unique_id = 'st'
df_wheat = pd.read_csv("df_wheat.csv",index_col=None)
df_index = pd.read_csv("df_index.csv",index_col=None)

#____________________________________________________________________________________________________________________________________________

#                                                   2_Nettoyage_Données
#____________________________________________________________________________________________________________________________________________

df_wheat = clean_df(df_wheat,commodite)
df_index = clean_df(df_index,'index')
df_wheat_2 = df_wheat.copy()

#____________________________________________________________________________________________________________________________________________

#                                                   3_Titre_+_Image
#____________________________________________________________________________________________________________________________________________

picture = get_picture(commodite)
title = "Investir dans le blé : entre opportunités et défis climatiques"
subtitle = "Analyse approfondie des tendances, performances et métriques clés du marché du blé"
display_header(picture, title, subtitle)
display_bar(df_wheat_2, commodite)
reverse_dataframe(df_wheat)

#____________________________________________________________________________________________________________________________________________

#                                                   4_Fusion_Tableaux+_Ajout_Indicateurs
#____________________________________________________________________________________________________________________________________________

sub_df_wheat = pd.concat([df_wheat, df_index], axis =1)
sub_df_wheat_ind = sub_df_wheat.copy()
df_ind(sub_df_wheat_ind, commodite)

#____________________________________________________________________________________________________________________________________________

#                                                   5_Séléction_Période
#____________________________________________________________________________________________________________________________________________

sub_df_wheat_ind_filtered = sub_df_wheat_ind.iloc[:13,:]

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

display_custom_table(df_wheat_2.iloc[:13,:], "Données descriptives sur le blé")
# Générer les graphiques
fig1, title1 = graph_cours_boursier(sub_df_wheat_ind_filtered, selected_commodity, commodite)
fig2 = graph_indicateurs(sub_df_wheat_ind_filtered, commodite, selected_indicators)

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
           Le marché du blé se trouve à un tournant décisif, influencé par des facteurs variés tels que les aléas climatiques, les tensions géopolitiques, et une demande mondiale croissante. Alors que les sécheresses et les épisodes de canicule dans les principales régions productrices, comme l’Amérique du Nord et l’Europe, mettent sous pression les rendements, les avancées technologiques en agriculture pourraient ouvrir de nouvelles perspectives d’efficacité.            <p style="text-align: justify;">
    
"""
)

#____________________________________________________________________________________________________________________________________________
