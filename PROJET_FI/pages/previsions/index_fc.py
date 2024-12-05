import requests #68S617QRYKZHX4ZN #I1TVUXGTKDYPXB78
import pandas as pd
import streamlit as st 
import plotly 
import numpy as np
import plotly.graph_objects as go
import altair as alt
import plotly.express as px
from datetime import datetime, timedelta
from features.functions import *
from features.layout import *
import os 

'''
Sommaire : 

1_Import_Données_+_Nettoyage_Données
2_2_Titre_&_Sidebar_Parametres
3_MOYENNE_MOBILE
4_LES
5_LED
6_HOL_&_WINTER

'''
#___________________________________________________________________________________________________________________________________

#                                                   1_Import_Données_+_Nettoyage_Données
#___________________________________________________________________________________________________________________________________

df_index = pd.read_csv("df_index.csv", index_col=None)
df_index = clean_df(df_index,'index')

df_index_mm = df_index.copy()
df_index_les = df_index.copy()
df_index_led = df_index.copy()
df_index_hw = df_index.copy()

#___________________________________________________________________________________________________________________________________

#                                                   2_Titre_&_Sidebar_Parametres
#___________________________________________________________________________________________________________________________________

def create_marquee(
    text, 
    speed=12, 
    font_size="26px", 
    text_color="#FFFFFF", 
    background_color="#000000", 
    font_family="Playfair Display"
):
    """
    Crée une animation de texte défilant (marquee).
    :param text: Le texte à afficher.
    :param speed: Vitesse de défilement en secondes.
    :param font_size: Taille de la police.
    :param text_color: Couleur du texte.
    :param background_color: Couleur de fond.
    :param font_family: Police utilisée pour le texte.
    :return: Code HTML stylisé pour Streamlit.
    """
    return f"""
    <style>
    @keyframes scroll-left {{
        0% {{ transform: translateX(100%); }}
        100% {{ transform: translateX(-100%); }}
    }}

    .marquee-container {{
        overflow: hidden;
        white-space: nowrap;
        background-color: {background_color};
        padding: 10px;
        border-radius: 5px;
    }}

    .marquee-text {{
        display: inline-block;
        font-size: {font_size};
        color: {text_color};
        font-family: '{font_family}', serif;
        animation: scroll-left {speed}s linear infinite;
    }}
    </style>

    <div class="marquee-container">
        <span class="marquee-text">{text}</span>
    </div>
    """

# Utilisation de la fonction
marquee_html = create_marquee(
    text="Prévisions de l'index : Anticipez les tendances du marché des commodités !",
    speed=12,
    font_size="26px",
    text_color="#FFFFFF",
    background_color="#000000",
    font_family="Playfair Display"
)

st.markdown(marquee_html, unsafe_allow_html=True)



forecast_horizon, alpha, beta, gamma, season_length = sidebar_parametres_previsions()

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

#___________________________________________________________________________________________________________________________________
    
#                                                   3_MOYENNE_MOBILE
#___________________________________________________________________________________________________________________________________

with col1:

    current_month_start = pd.to_datetime('today').replace(day=1)  # Remplace le jour par 1 pour obtenir le début du mois actuel

    df_index_mm.index = pd.date_range(start=current_month_start , periods=len(df_index_mm), freq='-1MS')  # Index mensuel descendant

    # Étape 2 : Calcul des prévisions avec un index d'extension
    last_date = df_index_mm.index[0]  # Première date historique
    forecast_index = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_horizon, freq='MS')

    # Prévisions de MM (Simples moyennes mobiles)
    df_mm = pd.DataFrame(
        moyenne_mobile_simple(df_index_mm['value_index'], 4, forecast_horizon),
        index=forecast_index,  # Index des prévisions
        columns=['MM']
    )

    # Étape 3 : Construire les deux parties
    # Partie historique : valeurs historiques, MM=NaN
    df_historical = df_index_mm.copy()
    df_historical['MM'] = np.nan

    # Partie prévisions : value_index=NaN, valeurs MM
    df_forecast = pd.DataFrame(index=forecast_index)
    df_forecast['value_index'] = np.nan
    df_forecast['MM'] = df_mm['MM']

    df_forecast = df_forecast[::-1]

    # Étape 4 : Concaténation des données historiques et des prévisions
    df_final = pd.concat([df_forecast, df_historical])

    # Étape 5 : Affichage dans Streamlit
    st.subheader('Prévision selon la méthode des moyennes mobiles')
    st.line_chart(df_final)

    add_horizontal_line(color="#FFF", thickness="3px")  # Ligne rouge de 3 pixels d'épaisseur
    add_horizontal_line(color="black", thickness="1px")    # Ligne noire fine


#___________________________________________________________________________________________________________________________________
 
#                                                   4_LES
#___________________________________________________________________________________________________________________________________

with col2:

    df_index_les.index = pd.date_range(start=current_month_start , periods=len(df_index_les), freq='-1MS')  # Index mensuel descendant

    # Étape 2 : Calcul des prévisions avec un index d'extension
    last_date = df_index_les.index[0]  # Première date historique (la plus récente)
    forecast_index = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_horizon, freq='MS')

    # Lissage exponentiel simple (modifié pour ordre décroissant)
    _, forecasts = lissage_exponentiel_simple(df_index_les['value_index'].values, alpha, forecast_horizon)

    # Étape 3 : Construire les deux parties du dataframe final
    # Partie historique : uniquement les données brutes historiques
    df_historical = df_index_les.copy()

    # Partie prévisions : uniquement les prévisions SES
    df_forecast = pd.DataFrame(index=forecast_index[::-1])  # Inverser l'ordre de l'index
    df_forecast['value_index'] = np.nan  # Aucune donnée brute pour les prévisions
    df_forecast['LES'] = forecasts        # Ajouter les prévisions SES

    # Étape 4 : Concaténation
    df_final = pd.concat([df_forecast, df_historical])

    # Étape 5 : Affichage
    st.subheader('Prévisions selon la méthode du Lissage Exponentiel Simple (LES)')
    st.line_chart(df_final[['value_index', 'LES']])

    add_horizontal_line(color="#FFF", thickness="3px")  # Ligne rouge de 3 pixels d'épaisseur
    add_horizontal_line(color="black", thickness="1px")    # Ligne noire fine


#___________________________________________________________________________________________________________________________________

#                                                   5_LED
#___________________________________________________________________________________________________________________________________

with col3:


    df_index_led.index = pd.date_range(start=current_month_start , periods=len(df_index_led), freq='-1MS')  # Index mensuel descendant

    # Étape 2 : Calcul des prévisions LED avec un index d'extension
    last_date = df_index_led.index[0]  # Première date historique (la plus récente)
    forecast_index = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_horizon, freq='MS')

    # Lissage exponentiel double (LED)
    _, forecasts = lissage_exponentiel_double(df_index_led['value_index'].values, alpha, beta, forecast_horizon)

    # Inverser les prévisions pour qu'elles aillent du futur au plus récent
    forecasts = forecasts[::-1]

    # Étape 3 : Construire les deux parties du dataframe final
    # Partie historique : uniquement les données brutes historiques
    df_historical = df_index_led.copy()

    # Partie prévisions : uniquement les prévisions LED
    df_forecast = pd.DataFrame(index=forecast_index[::-1])  # Inverser l'ordre de l'index
    df_forecast['value_index'] = np.nan  # Aucune donnée brute pour les prévisions
    df_forecast['LED'] = forecasts        # Ajouter les prévisions LED

    # Étape 4 : Concaténation
    df_final = pd.concat([df_forecast, df_historical])

    # Étape 5 : Affichage
    st.subheader('Prévisions selon la méthode du Lissage Exponentiel Simple (LED)')
    st.line_chart(df_final[['value_index', 'LED']])

    add_horizontal_line(color="#FFF", thickness="3px")  # Ligne rouge de 3 pixels d'épaisseur
    add_horizontal_line(color="black", thickness="1px")    # Ligne noire fine


#___________________________________________________________________________________________________________________________________

#                                                   6_HOL_&_WINTER
#___________________________________________________________________________________________________________________________________

with col4:


    # Étape 1 : Configuration de l'index mensuel descendant pour les données historiques
    df_index_hw.index = pd.date_range(start='2024-09', periods=len(df_index_hw), freq='-1MS')  # Index mensuel descendant

    # Étape 2 : Calcul des prévisions Holt-Winters avec un index d'extension
    last_date = df_index_hw.index[0]  # Première date historique (la plus récente)
    forecast_index = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_horizon, freq='MS')


    # Validation de la longueur des données par rapport à la saisonnalité
    if len(df_index_hw) < season_length:
        st.error("Les données historiques doivent contenir au moins autant d'observations que la saisonnalité.")
    else:
        # Prévisions avec Holt-Winters
        _, forecasts = holt_winters(df_index_hw['value_index'].values, alpha, beta, gamma, season_length, forecast_horizon)

        # Inverser les prévisions pour qu'elles aillent du futur au présent
        forecasts = forecasts[::-1]

        # Étape 3 : Construire les deux parties du dataframe final
        # Partie historique : uniquement les données brutes historiques
        df_historical = df_index_hw.copy()

        # Partie prévisions : uniquement les prévisions HW
        df_forecast = pd.DataFrame(index=forecast_index[::-1])  # Inverser l'ordre de l'index
        df_forecast['value_index'] = np.nan  # Aucune donnée brute pour les prévisions
        df_forecast['HW'] = forecasts         # Ajouter les prévisions Holt-Winters

        # Étape 4 : Concaténation
        df_final = pd.concat([df_forecast, df_historical])

        # Étape 5 : Affichage
    st.subheader('Prévisions selon la méthode de Holt & Winter')
    st.line_chart(df_final[['value_index', 'HW']])
    
    add_horizontal_line(color="#FFF", thickness="3px")  # Ligne rouge de 3 pixels d'épaisseur
    add_horizontal_line(color="black", thickness="1px")    # Ligne noire fine


#___________________________________________________________________________________________________________________________________
