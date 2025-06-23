import requests #68S617QRYKZHX4ZN #I1TVUXGTKDYPXB78
import pandas as pd
import streamlit as st 
import plotly 
import numpy as np
import plotly.graph_objects as go
import altair as alt
import plotly.express as px
from datetime import datetime, timedelta
import os
from features.functions import *

#TAILLE DE LA PAGE
st.set_page_config(
    layout="wide",  #pour maximiser l'espace
)
#_______________________________________________________________________________________________________________________

# Ajouter du style CSS pour styliser les cartes
st.markdown(
    """
    <style>
    .card {
        background-color: #F6F3F1;
        color: black;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Ombre légère */
        padding: 15px; /* Espace intérieur */
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        overflow: hidden;
        cursor: pointer;
        height: 100px; /* Hauteur initiale */
    }

    .card:hover {
        transform: scale(1.05); /* Agrandit légèrement au survol */
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15); /* Accentue l'ombre */
        height: auto; /* Affiche tout le contenu */
    }

    .card h2 {
        font-size: 1em; /* Taille du titre */
        color: #007BFF;
        margin-bottom: 5px;
    }

    .card p {
        font-size: 0.9em; /* Taille réduite du texte */
        line-height: 1.4;
        color: #333;
        margin: 0;
        display: none; /* Cache le texte par défaut */
    }

    .card:hover p {
        display: block; /* Affiche le texte au survol */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Définir les données des cartes
cards = [
    {
        "title": "Café",
        "content": "Le café est cultivé principalement dans les régions tropicales, avec des producteurs majeurs tels que le Brésil, le Vietnam et la Colombie. Le prix du café est influencé par des facteurs tels que la météo, les récoltes, et les tendances de consommation.",
    },

    {
        "title": "Sucre",
        "content": "Le sucre est un ingrédient clé dans l'industrie alimentaire et est utilisé mondialement. Les prix du sucre peuvent être influencés par des facteurs climatiques, des changements dans les politiques agricoles, et des mouvements de la demande mondiale.",
    },
    {
        "title": "Maïs",
        "content": "Le maïs est particulièrement sensible aux variations climatiques et aux changements dans les habitudes alimentaires. Il est également utilisé pour la production de biocarburants, ce qui en fait une ressource agricole stratégique.",
    },
    {
        "title": "Blé",
        "content": "Le blé est largement utilisé dans la production de pains, de pâtes et de nombreux autres aliments de base. Ses prix peuvent fluctuer en fonction des conditions climatiques et des politiques agricoles des pays producteurs.",
    },
]

# Utiliser les colonnes de Streamlit pour aligner les cartes sur 4 colonnes
cols = st.columns(4)

# Afficher chaque carte dans sa propre colonne
for i, card in enumerate(cards):
    with cols[i]:
        st.markdown(
            f"""
            <div class="card">
                <h2>{card['title']}</h2>
                <p>{card['content']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.subheader("")

marquee_html = """
<div style="overflow: hidden; white-space: nowrap; background-color: #FFFFFF; padding: 10px; border: 0px solid #ddd;">
    <span style="display: inline-block; font-size: 24px; color: #000000; font-weight: bold; animation: scroll-left 10s linear infinite;">
       Analyse Technique : Étapes pour Identifier une Tendance
    </span>
</div>

<style>
@keyframes scroll-left {
  0% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(-100%);
  }
}
span {
  animation: scroll-left 5s linear infinite;
}
</style>
"""

# Insère le HTML dans Streamlit
st.components.v1.html(marquee_html, height=50)

# Création des onglets pour chaque indicateur
onglet_mm, onglet_rsi, onglet_stoch = st.tabs(["Moyenne Mobile (MM)", "RSI", "Stochastique"])

# Contenu pour la Moyenne Mobile
with onglet_mm:
    st.markdown(
        "<h1 style='font-size:  20px;'> Moyenne Mobile (MM)</h1>",
        unsafe_allow_html=True
    )
    st.write(
        """
        La Moyenne Mobile est un indicateur qui permet de lisser les données de prix pour dégager une tendance.
        Elle est utilisée pour identifier la direction du marché et les niveaux de support et de résistance.
        
        **Exemple :**
        - Une moyenne mobile à 20 jours lisse les prix sur les 20 derniers jours.
        - Une croissance de la moyenne mobile indique une tendance haussière.
        - Une baisse de la moyenne mobile indique une tendance baissière.
        """
    )
    st.markdown("**Application pratique :** Utilisée pour détecter les points d'entrée ou de sortie en fonction des tendances globales.")

# Contenu pour le RSI
with onglet_rsi:
    st.markdown(
        "<h1 style='font-size:  20px;'>RSI (Relative Strength Index)</h1>",
        unsafe_allow_html=True
    )
    st.write(
        """
        Le RSI est un indicateur de momentum qui mesure la vitesse et le changement des mouvements de prix.
        Il oscille entre 0 et 100 et est utilisé pour déterminer si un actif est en zone de surachat ou de survente.
        
        **Exemple :**
        - RSI > 70 : Zone de surachat. Le marché est probablement surévalué.
        - RSI < 30 : Zone de survente. Le marché est probablement sous-évalué.
        """
    )
    st.markdown("**Application pratique :** Utilisé pour identifier des retournements potentiels de tendance.")

# Contenu pour le Stochastique
with onglet_stoch:
    st.markdown(
        "<h1 style='font-size:  20px;'>Stochastique</h1>",
        unsafe_allow_html=True
    )
    st.write(
        """
        L'indicateur Stochastique mesure la relation entre le prix de clôture d'un actif et son range de prix
        sur une période donnée. Il oscille également entre 0 et 100.
        
        **Exemple :**
        - Stochastique > 80 : Zone de surachat. Un retournement baissier est probable.
        - Stochastique < 20 : Zone de survente. Un retournement haussier est probable.
        """
    )
    st.markdown("**Application pratique :** Utilisé pour confirmer les signaux de surachat et survente détectés par d'autres indicateurs.")

marquee_html = """
<div style="overflow: hidden; white-space: nowrap; background-color: #FFFFF; padding: 10px; border: 0px solid #ddd;">
    <span style="display: inline-block; font-size: 24px; color: #000000; font-weight: bold; animation: scroll-left 10s linear infinite;">
       Méthodes de Prévisions: Analyser, Lisser, Anticiper
    </span>
</div>

<style>
@keyframes scroll-left {
  0% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(-100%);
  }
}
span {
  animation: scroll-left 5s linear infinite;
}
</style>
"""
# Insère le HTML dans Streamlit
st.components.v1.html(marquee_html, height=50)

# Ajout de style CSS pour personnaliser les onglets
st.markdown(
    """
    <style>
    div[data-testid="stTabs"] > div {
        font-size: 18px; /* Taille de police pour les onglets */
        font-weight: bold; /* Onglets en gras */
        color: #00000; /* Couleur du texte */
    }

    div[data-testid="stTabs"] > div > div[aria-selected="true"] {
        color: #007BFF; /* Couleur pour l'onglet actif */
        border-bottom: 3px solid #007BFF; /* Ligne bleue sous l'onglet actif */
    }

    div[data-testid="stTabs"] > div > div[aria-selected="false"] {
        color: #666666; /* Couleur pour les onglets inactifs */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Création des onglets pour chaque méthode
onglet_mm, onglet_les, onglet_led, onglet_holt_winter = st.tabs([
    "Moyenne Mobile (MM)", 
    "Lissage Exponentiel Simple (LES)", 
    "Lissage Exponentiel Double (LED)", 
    "Holt & Winter"
])

# Contenu pour chaque méthode
with onglet_mm:
    st.markdown(
        "<h1 style='font-size:  20px;'>Moyenne Mobile (MM)</h1>",
        unsafe_allow_html=True
    )
    st.write(
        """
        La méthode des moyennes mobiles est une technique statistique utilisée pour lisser les séries temporelles
        et rendre plus visibles les tendances sous-jacentes en éliminant les variations aléatoires. Elle consiste à 
        calculer la moyenne d’un ensemble de données sur une période fixe (par exemple, les 4 derniers mois) et 
        à faire glisser cette fenêtre de moyenne à travers la série temporelle.
        
        **Points Clés :**
        - Utile pour des séries sans tendance marquée ou saisonnalité.
        - Peut avoir du mal à capturer des changements rapides dans les données.
        """
    )

with onglet_les:
    st.markdown(
        "<h1 style='font-size:  20px;'>Lissage Exponentiel Simple (LES)</h1>",
        unsafe_allow_html=True
    )
    st.write(
        """
        Le lissage exponentiel simple (ou Simple Exponential Smoothing, SES) est une méthode qui attribue 
        un poids décroissant aux observations passées, ce qui permet de donner plus d'importance aux valeurs 
        récentes de la série temporelle.
        
        **Points Clés :**
        - Prévision basée sur une combinaison pondérée des valeurs passées.
        - Contrôle de l'importance des données récentes via le paramètre alpha (0 à 1).
        - Idéal pour des séries sans tendance ni saisonnalité.
        """
    )

with onglet_led:
    st.markdown(
        "<h1 style='font-size:  20px;'>Lissage Exponentiel Double (LED)</h1>",
        unsafe_allow_html=True
    )
    st.write(
        """
        Le lissage exponentiel double (ou Double Exponential Smoothing, DES) est une extension du lissage exponentiel simple,
        conçue pour traiter des séries temporelles qui présentent une tendance.
        
        **Points Clés :**
        - Utilise deux paramètres :
            - **Alpha** : pondère les données récentes.
            - **Beta** : modélise la tendance.
        - Prévision adaptée aux séries avec des changements à long terme.
        """
    )

with onglet_holt_winter:
    st.markdown(
        "<h1 style='font-size:  20px;'>Holt & Winter</h1>",
        unsafe_allow_html=True
    )
    st.write(
        """
        Les méthodes de Holt et Winter (ou Holt-Winters) sont des modèles avancés de lissage exponentiel qui permettent 
        de prendre en compte à la fois une tendance et une saisonnalité dans les séries temporelles.
        
        **Points Clés :**
        - Holt ajuste le niveau et la tendance avec deux paramètres : **Alpha** et **Beta**.
        - Winter ajoute un troisième paramètre : **Gamma**, pour modéliser la saisonnalité.
        - Particulièrement utile pour les séries présentant des cycles réguliers (par exemple, des ventes saisonnières).
        """
    )


