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

df_wheat = pd.read_csv("df_wheat.csv", index_col=None)
df_corn = pd.read_csv("df_corn.csv", index_col=None)
df_coffee = pd.read_csv("df_coffee.csv", index_col=None)
df_index = pd.read_csv("df_index.csv", index_col=None)
df_sugar = pd.read_csv("df_sugar.csv", index_col=None)

df_index = clean_df(df_index,'index')
df_coffee = clean_df(df_coffee,'coffee')
df_sugar = clean_df(df_sugar,'sugar')
df_corn = clean_df(df_corn,'corn')
df_wheat = clean_df(df_wheat,'wheat')

df_coffee_mm = df_coffee.copy()
df_coffee_les = df_coffee.copy()
df_coffee_led = df_coffee.copy()
df_coffee_hw = df_coffee.copy()

df_sugar_mm = df_sugar.copy()
df_sugar_les = df_sugar.copy()
df_sugar_led = df_sugar.copy()
df_sugar_hw = df_sugar.copy()

df_corn_mm = df_corn.copy()
df_corn_les = df_corn.copy()
df_corn_led = df_corn.copy()
df_corn_hw = df_corn.copy()

df_wheat_mm = df_wheat.copy()
df_wheat_les = df_wheat.copy()
df_wheat_led = df_wheat.copy()
df_wheat_hw = df_wheat.copy()

df_index_mm = df_index.copy()
df_index_les = df_index.copy()
df_index_led = df_index.copy()
df_index_hw = df_index.copy()

df_dict_mm = {
    'coffee': df_coffee_mm,
    'sugar': df_sugar_mm,
    'corn': df_corn_mm,
    'wheat': df_wheat_mm,
    'index': df_index_mm
}

df_dict_les = {
    'coffee': df_coffee_les,
    'sugar': df_sugar_les,
    'corn': df_corn_les,
    'wheat': df_wheat_les,
    'index': df_index_les
}

df_dict_led = {
    'coffee': df_coffee_led,
    'sugar': df_sugar_led,
    'corn': df_corn_led,
    'wheat': df_wheat_led,
    'index': df_index_led
}

df_dict_hw = {
    'coffee': df_coffee_hw,
    'sugar': df_sugar_hw,
    'corn': df_corn_hw,
    'wheat': df_wheat_hw,
    'index': df_index_hw
}


#___________________________________________________________________________________________________________________________________

#                                                   2_Titre_&_Sidebar_Parametres
#___________________________________________________________________________________________________________________________________



forecast_horizon, alpha, beta, gamma, season_length = sidebar_parametres_previsions()

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
    text="Prévisions : Anticipez les tendances du marché des commodités !",
    speed=12,
    font_size="26px",
    text_color="#FFFFFF",
    background_color="#000000",
    font_family="Playfair Display"
)

st.markdown(marquee_html, unsafe_allow_html=True)


col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

#___________________________________________________________________________________________________________________________________
    
#                                                   3_MOYENNE_MOBILE
#___________________________________________________________________________________________________________________________________

with col1:
    selected_commodities_mm = st.sidebar.multiselect("Sélectionnez les indicateurs à afficher pour la MM", 
                                        ['MM_coffee','MM_sugar','MM_corn','MM_wheat','MM_index',], 
                                        default=['MM_coffee','MM_sugar','MM_corn','MM_wheat','MM_index',])


    fig_mm = generate_mm_forecasts_and_plot(df_dict_mm, forecast_horizon, selected_commodities_mm)

    # Affichage dans Streamlit
    st.plotly_chart(fig_mm)

    # Exemple d'utilisation
    add_horizontal_line(color="#FFF", thickness="3px")  # Ligne rouge de 3 pixels d'épaisseur
    add_horizontal_line(color="black", thickness="1px")    # Ligne noire fine

#___________________________________________________________________________________________________________________________________
 
#                                                   4_LES
#___________________________________________________________________________________________________________________________________

with col2:

    selected_commodities_les = st.sidebar.multiselect(
        "Sélectionnez les indicateurs à afficher pour le LES",
        ['LES_coffee', 'LES_sugar', 'LES_corn', 'LES_wheat', 'LES_index'],
        default=['LES_coffee', 'LES_sugar', 'LES_corn', 'LES_wheat', 'LES_index']
    )

    # Génération du graphique
    fig_les = generate_les_forecasts_and_plot(df_dict_les, forecast_horizon, alpha, selected_commodities_les)

    # Affichage dans Streamlit
    st.plotly_chart(fig_les)


    # Exemple d'utilisation
    add_horizontal_line(color="#FFF", thickness="3px")  # Ligne rouge de 3 pixels d'épaisseur
    add_horizontal_line(color="black", thickness="1px")    # Ligne noire fine

#___________________________________________________________________________________________________________________________________

#                                                   5_LED
#___________________________________________________________________________________________________________________________________

with col3:


    selected_commodities_led = st.sidebar.multiselect("Sélectionnez les indicateurs à afficher pour le LED", 
                                        ['LED_coffee','LED_sugar','LED_corn','LED_wheat','LED_index',], 
                                        default=['LED_coffee','LED_sugar','LED_corn','LED_wheat','LED_index',])

    fig_led = generate_led_forecasts_and_plot(df_dict_led, forecast_horizon, alpha, beta, selected_commodities_led)
    # Affichage dans Streamlit
    st.plotly_chart(fig_led)


    # Exemple d'utilisation
    add_horizontal_line(color="#FFF", thickness="3px")  # Ligne rouge de 3 pixels d'épaisseur
    add_horizontal_line(color="black", thickness="1px")    # Ligne noire fine

#___________________________________________________________________________________________________________________________________

#                                                   6_HOL_&_WINTER
#___________________________________________________________________________________________________________________________________

with col4:


    selected_commodities_hw = st.sidebar.multiselect("Sélectionnez les indicateurs à afficher pour le H&W", 
                                        ['H&W_coffee','H&W_sugar','H&W_corn','H&W_wheat','H&W_index',], 
                                        default=['H&W_coffee','H&W_sugar','H&W_corn','H&W_wheat','H&W_index',])

    fig_hw = generate_hw_forecasts_and_plot(df_dict_hw, forecast_horizon, alpha, beta, gamma, season_length, selected_commodities_hw)
    # Affichage dans Streamlit
    st.plotly_chart(fig_hw)

    # Exemple d'utilisation
    add_horizontal_line(color="#FFF", thickness="3px")  # Ligne rouge de 3 pixels d'épaisseur
    add_horizontal_line(color="black", thickness="1px")    # Ligne noire fine

#___________________________________________________________________________________________________________________________________
