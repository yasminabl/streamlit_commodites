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
6_Barre_defilante_affiche_bar
7_Bouton_Paramètre_Prévisions
8_Modifie_Affichage_Tableau_Conclusion
9_Titre_Prevision
10_Ajoute_Ligne
11_Titre_ All

'''
#___________________________________________________________________________________________________________________________________________

#                                                   1_Recupere_image_jpeg
#___________________________________________________________________________________________________________________________________________

def get_picture(commodite):
    dossier = 'pages/picture/'
    picture_name = generer_nom_image(commodite)
    picture_path = os.path.join(dossier, picture_name)
    picture = get_image_base64(picture_path) 
    return picture

#___________________________________________________________________________________________________________________________________________

#                                                   2_Affiche_l'en-tete
#___________________________________________________________________________________________________________________________________________

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
#___________________________________________________________________________________________________________________________________________

#                                                   3_Barre_defilante_calcul_metric
#___________________________________________________________________________________________________________________________________________


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

#___________________________________________________________________________________________________________________________________________

#                                                   4_Barre_defilante_icone_&_style
#___________________________________________________________________________________________________________________________________________

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

#___________________________________________________________________________________________________________________________________________

#                                                   5_Barre_defilante_html_content
#___________________________________________________________________________________________________________________________________________

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
#___________________________________________________________________________________________________________________________________________

#                                                   6_Barre_defilante_affiche_bar
#___________________________________________________________________________________________________________________________________________


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

#___________________________________________________________________________________________________________________________________________

#                                                   7_Bouton_Paramètre_Prévisions
#___________________________________________________________________________________________________________________________________________

def sidebar_parametres_previsions():
    """
    Fonction pour afficher la sidebar avec les paramètres de prévision
    et récupérer les valeurs des entrées de l'utilisateur.
    """

    # Application de CSS personnalisé via HTML
    st.markdown("""
        <style>
            /* Conteneur principal */
            .main-container {
                background-color: #f0f4f8;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }

            /* Section des prévisions */
            .forecast-section {
                background-color: #ecf0f1;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
            }

            .forecast-section h2 {
                font-size: 24px;
                color: #2980b9;
            }

            /* Style des sliders et titres */
            .sidebar .stSlider, .stNumberInput {
                margin-bottom: 10px;
                font-size: 16px;
            }

            .sidebar .stSlider .stSliderTrack {
                background-color: #2980b9;
                height: 10px;
                border-radius: 5px;
            }

            .sidebar .stNumberInput input {
                padding: 5px;
                border-radius: 5px;
                border: 1px solid #2980b9;
                margin-top: 5px;
            }

            /* Sidebar */
            .sidebar .sidebar-content {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Affichage du titre dans la sidebar
    st.sidebar.markdown("<h2>Choix des paramètres</h2>", unsafe_allow_html=True)

    # Choix du nombre de mois à prévoir
    forecast_horizon = st.sidebar.slider(
        'Entrez le nombre de mois à prévoir :', 
        min_value=1,  # Valeur minimale de 1 mois
        max_value=24,  # Valeur maximale de 24 mois
        value=12,  # Valeur par défaut
        step=1,  # Incrément de 1 pour chaque pas
        format="%d mois"  # Format de l'étiquette
    )

    # Choix des paramètres alpha, beta, gamma et season_length
    st.sidebar.markdown("**Alpha (composant de tendance) :**")
    alpha = st.sidebar.slider(
        'Alpha:',
        min_value=0.0,  # Valeur minimale
        max_value=1.0,  # Valeur maximale
        value=0.4,  # Valeur par défaut
        step=0.1  # Incrément de 0.1
    )

    st.sidebar.markdown("**Beta (tendance linéaire) :**")
    beta = st.sidebar.slider(
        'Beta:',
        min_value=0.0,  # Valeur minimale
        max_value=1.0,  # Valeur maximale
        value=0.1,  # Valeur par défaut
        step=0.1  # Incrément de 0.1
    )

    st.sidebar.markdown("**Gamma (saisonnalité) :**")
    gamma = st.sidebar.slider(
        'Gamma:',
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.1
    )

    st.sidebar.markdown("**Saisonnalité (en mois) :**")
    season_length = st.sidebar.slider(
        'Longueur saisonnière:',
        min_value=1,  # Valeur minimale de 1 mois
        max_value=12,  # Valeur maximale de 12 mois
        value=12,  # Valeur par défaut
        step=1  # Incrément de 1 pour chaque pas
    )

    # Retourne les valeurs des paramètres pour une utilisation dans d'autres pages
    return forecast_horizon, alpha, beta, gamma, season_length

#___________________________________________________________________________________________________________________________________________

#                                                   8_Modifie_Affichage_Tableau_Conclusion
#___________________________________________________________________________________________________________________________________________

def highlight_tendance(val, row):
    """Appliquer un style spécifique pour la ligne 'Tendance'."""
    # Appliquer la couleur verte pour 'Haussière', sinon rouge pour 'Baissière'
    if row == 'Tendance':
        if val == 'Haussière':
            return 'color: green'
        elif val == 'Baissière':
            return 'color: red'
    return ''  # Pas de changement de couleur pour les autres lignes

def highlight_prevision(val, row):
    """Appliquer un style spécifique pour la ligne 'Prévision'."""
    # Appliquer la couleur verte pour 'Hausse', sinon rouge pour 'Baisse'
    if row == 'Prévision':
        if val == 'Hausse':
            return 'color: green'
        elif val == 'Baisse':
            return 'color: red'
    return ''  # Pas de changement de couleur pour les autres lignes

def highlight_pressions(val, row):
    """Appliquer un style spécifique pour la ligne 'Pression'."""
    # Appliquer la couleur verte pour 'Achat' et rouge pour 'Vente'
    if row == 'Pression':
        if val == 'Vente':
            return 'color: red'
        elif val == 'Achat':
            return 'color: green'
    return ''  # Pas de changement de couleur pour les autres lignes

def apply_styles(df_conclusion):
    """Appliquer les styles conditionnels aux lignes spécifiques."""
    # Appliquer un style conditionnel pour chaque ligne (Tendance, Pression, Prévision)
    # Utiliser apply avec axis=1 pour parcourir les lignes
    df_conclusion_styled = df_conclusion.style.apply(
        lambda row: [highlight_tendance(val, 'Tendance') for val in row],
        axis=1, subset=['coffee', 'sugar', 'corn', 'wheat', 'index']
    )
    
    df_conclusion_styled = df_conclusion_styled.apply(
        lambda row: [highlight_prevision(val, 'Prévision') for val in row],
        axis=1, subset=['coffee', 'sugar', 'corn', 'wheat', 'index']
    )
    
    df_conclusion_styled = df_conclusion_styled.apply(
        lambda row: [highlight_pressions(val, 'Pression') for val in row],
        axis=1, subset=['coffee', 'sugar', 'corn', 'wheat', 'index']
    )

    return df_conclusion_styled


#___________________________________________________________________________________________________________________________________________

#                                                   9_Titre_Prevision
#___________________________________________________________________________________________________________________________________________

def create_marquee(title_text, speed=10, color="#FFFFFF", font_size="24px"):
    """
    Crée un titre défilant (marquee) pour Streamlit.

    :param title_text: Texte à afficher dans le titre défilant.
    :param speed: Durée en secondes pour une boucle complète (vitesse).
    :param color: Couleur du texte (code hexadécimal ou nom CSS).
    :param font_size: Taille de la police du texte (ex. '24px', '1.5em').
    """
    marquee_html = f"""
    <style>
    .marquee {{
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        box-sizing: border-box;
    }}
    .marquee span {{
        display: inline-block;
        padding-left: 100%; /* Démarre hors de l'écran */
        animation: marquee {speed}s linear infinite; /* Durée définie par l'utilisateur */
        font-size: {font_size};
        font-weight: bold;
        color: {color};
    }}
    @keyframes marquee {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-100%); }} /* Fait défiler tout le texte */
    }}
    </style>
    <div class="marquee">
        <span>{title_text}</span>
    </div>
    """
    return marquee_html

#___________________________________________________________________________________________________________________________________________

#                                                   10_Ajoute_Ligne
#___________________________________________________________________________________________________________________________________________

def add_horizontal_line(color="#FFFFFF", thickness="2px"):
    """
    Ajoute une ligne horizontale qui prend toute la largeur de la page.
    
    :param color: Couleur de la ligne (en code hexadécimal ou nom CSS, par exemple "#FFFFFF" ou "black").
    :param thickness: Épaisseur de la ligne (par exemple "2px").
    """
    st.markdown(
        f"""
        <hr style="border: none; border-top: {thickness} solid {color}; margin: 20px 0;" />
        """,
        unsafe_allow_html=True
    )

#___________________________________________________________________________________________________________________________________

#                                                   11_Titre_ All
#___________________________________________________________________________________________________________________________________

def display_styled_title(title_text, font_size="22px", font_color="#FFFFFF", underline_color="#FFFF", underline_width="20px", font_family="Playfair Display"):
    # Importer la police depuis Google Fonts
    st.markdown(
        f"""
        <link href="https://fonts.googleapis.com/css2?family={font_family.replace(' ', '+')}:wght@400;700&display=swap" rel="stylesheet">
        <div style="text-align: left; margin-bottom: 16px;">
            <h1 style="font-size: {font_size}; color: {font_color}; font-family: '{font_family}', sans-serif; margin-bottom: 10px;">
                {title_text}
            </h1>
            <div style="width: {underline_width}; height: 2px; background-color: {underline_color}; margin: 0 auto;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

#___________________________________________________________________________________________________________________________________


