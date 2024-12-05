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
1_Recupere_image_jpeg
2_Affiche_l'en-tete
3_Barre_defilante_calcul_metric
4_Barre_defilante_icone_&_style
5_Barre_defilante_html_content

'''

 #__________________________________________1_Recupere_image_jpeg___________________________________________________________

def get_picture(commodite):
    dossier = 'pages/picture/'
    picture_name = generer_nom_image(commodite)
    picture_path = os.path.join(dossier, picture_name)
    picture = get_image_base64(picture_path) 
    return picture


 #__________________________________________2_Affiche_l'en-tete___________________________________________________________
def display_header(picture, title, subtitle):
    # Ajouter les styles CSS directement
    st.markdown("""
        <style>
            /* Importation de la police Playfair Display */
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

            /* Conteneur principal */
            .header-container {
                display: flex;
                align-items: center; /* Aligne l'image et le texte verticalement */
                gap: 20px; /* Espacement entre l'image et le texte */
                margin-top: 20px;
            }

            /* Style de l'image */
            .centered-image {
                width: 150px; /* Taille de l'image réduite */
                height: auto; /* Conserve les proportions */
                display: block;
            }

            /* Conteneur du texte */
            .text-container {
                text-align: left; /* Texte aligné à gauche */
            }

            /* Style du titre principal */
            .main-title {
                font-size: 28px; /* Taille du titre */
                font-weight: bold;
                font-family: 'Playfair Display', serif; /* Utilisation de la police Playfair Display */
                color: #ffffff;
                margin: 0;
            }

            /* Ligne décorative sous le titre */
            .line {
                width: 200px; /* Largeur de la ligne */
                height: 1px; /* Épaisseur de la ligne */
                background-color: #ffffff;
                margin: 10px 0;
            }

            /* Sous-titre */
            .main-subtitle {
                font-size: 14px; /* Taille du sous-titre */
                font-family: 'Poppins', sans-serif; /* Police secondaire pour le sous-titre */
                color: #bbbbbb; /* Gris clair */
                margin: 0;
            }
        </style>
    """, unsafe_allow_html=True)

    # Ajouter le contenu HTML avec l'image, le titre et le sous-titre
    st.markdown(f"""
        <div class="header-container">
            <div class="image-container">
                <img src="data:image/png;base64,{picture}" alt="Image" class="centered-image">
            </div>
            <div class="text-container">
                <h1 class="main-title">{title}</h1>
                <div class="line"></div>
                <p class="main-subtitle">{subtitle}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

 #__________________________________________3_Barre_defilante_calcul_metric___________________________________________________________


def calculate_metrics(df,commodite):
    # Conversion de l'index en datetime si nécessaire
    df.index = pd.to_datetime(df.index, errors='coerce')

    # Calcul du taux de fermeture mensuel
    df_monthly = df.resample('M').last()
    df_monthly['Taux_Fermeture'] = df_monthly[f'value_{commodite}']

    # Calcul du pourcentage de variation par rapport à l'année précédente
    df_monthly['Variation_%'] = df_monthly['Taux_Fermeture'].pct_change(12) * 100

    # Calcul de la volatilité mensuelle
    volatility_monthly = df_monthly['Taux_Fermeture'].pct_change().std()

    # Valeurs actuelles
    current_rate = df_monthly['Taux_Fermeture'].iloc[-1] if not df_monthly['Taux_Fermeture'].empty else np.nan
    previous_year_rate = (
        df_monthly['Taux_Fermeture'].shift(12).iloc[-1] if not df_monthly['Taux_Fermeture'].shift(12).empty else np.nan
    )
    
    # Variation en pourcentage
    percentage_change = (
        ((current_rate - previous_year_rate) / previous_year_rate * 100) if previous_year_rate else np.nan
    )
    
    return df_monthly, current_rate, previous_year_rate, percentage_change, volatility_monthly

 #__________________________________________4_Barre_defilante_icone_&_style___________________________________________________________

def determine_icons_and_styles(percentage_change, volatility_monthly, df_monthly):
    # Détermine l'icône de flèche et les styles de variation
    if not np.isnan(percentage_change):
        if percentage_change > 0:
            arrow_icon = '<i class="fas fa-arrow-up" style="color: green;"></i>'
            percentage_style = "color: green;"
        elif percentage_change < 0:
            arrow_icon = '<i class="fas fa-arrow-down" style="color: red;"></i>'
            percentage_style = "color: red;"
        else:
            arrow_icon = ''
            percentage_style = "color: black;"
    else:
        arrow_icon = ''
        percentage_style = "color: black;"

    # Détermine la tendance
    trend = (
        "Haussiere" if (df_monthly['Taux_Fermeture'].diff() > 0).iloc[-3:].all()
        else "Baissiere"
    )
    trend_style = "color: green;" if trend == "Haussiere" else "color: red;"

    # Détermine la performance
    performance = (
        "Stable" if volatility_monthly < 0.02
        else "Volatil" if 0.02 <= volatility_monthly < 0.05
        else "Très volatil"
    )
    performance_style = (
        "color: green;" if performance == "Stable"
        else "color: orange;" if performance == "Volatil"
        else "color: darkred;"
    )

    return arrow_icon, percentage_style, trend, trend_style, performance, performance_style

#__________________________________________5_Barre_defilante_html_content___________________________________________________________

def generate_html_content(
    current_rate_display, 
    volatility_monthly_display, 
    tendance_display, 
    trend_style, 
    performance_display, 
    performance_style
):
    contenu = f"""
    <div class='barre-defilante'>
        <span>
            <div class="rate-card">
                <div><i class="fas fa-dollar-sign"></i> Prix clôture</div>
                <div class="rate-value">{current_rate_display}</div>
            </div>
        </span>
        <span class="separator">|</span>
        <span>
            <div class="rate-card">
                <div><i class="fas fa-chart-line"></i> Volatilité mensuelle</div>
                <div class="rate-value">{volatility_monthly_display}</div>
            </div>
        </span>
        <span class="separator">|</span>
        <span>
            <div class="rate-card">
                <div><i class="fas fa-arrow-up"></i> Tendance</div>
                <div class="rate-value" style="{trend_style}">{tendance_display}</div>
            </div>
        </span>
        <span class="separator">|</span>
        <span>
            <div class="rate-card">
                <div><i class="fas fa-exclamation-triangle"></i> Performance</div>
                <div class="rate-value" style="{performance_style}">{performance_display}</div>
            </div>
        </span>
    </div>
    """
    return contenu

 #__________________________________________5_Barre_defilante_affiche_bar___________________________________________________________


def display_bar(df, commodite ):
    # Calcul des métriques
    df_monthly, current_rate, _, percentage_change, volatility_monthly = calculate_metrics(df,commodite)

    # Déterminer les styles et tendances
    (
        arrow_icon,
        percentage_style,
        trend,
        trend_style,
        performance,
        performance_style,
    ) = determine_icons_and_styles(percentage_change, volatility_monthly, df_monthly)

    # Valeurs actuelles formatées
    current_rate_display = f"{current_rate:.2f}$" if not np.isnan(current_rate) else "N/A"
    volatility_monthly_display = f"{volatility_monthly:.2f}%"
    tendance_display = trend
    performance_display = performance

    # Génération du contenu HTML
    contenu = generate_html_content(
        current_rate_display,
        volatility_monthly_display,
        tendance_display,
        trend_style,
        performance_display,
        performance_style,
    )

    # CSS global pour la barre défilante
    st.markdown("""
    <style>
    .barre-defilante {
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        display: flex;
        align-items: center;
        animation: defilement 15s linear infinite;
    }

    .rate-card {
        display: inline-block;
        text-align: center;
        padding: 10px 15px;
        background-color: #222;
        border-radius: 8px;
        color: white;
        font-size: 14px;
    }

    .separator {
        margin: 0 10px;
        color: #bbb;
    }

    @keyframes defilement {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    </style>
    """, unsafe_allow_html=True)

    # CSS pour les icônes
    st.markdown("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
    """, unsafe_allow_html=True)

    # Affichage de la barre défilante
    st.markdown(contenu, unsafe_allow_html=True)


