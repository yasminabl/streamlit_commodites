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
from features.layout import *
from io import StringIO

st.set_page_config(
    layout="wide",  #pour maximiser l'espace
)



def create_df(name, url, key):
    complete_url = f'{url}&apikey={key}'
    r = requests.get(complete_url)
    data = r.json()

    # Création du DataFrame
    df = pd.DataFrame(data['data'])  # Si les données pertinentes sont dans la clé 'data'
    df[f'{name}'] = name
    # Si les sous-dictionnaires contiennent 'date' et 'value', on les extrait
    df['date'] = df.apply(lambda x: x['date'], axis=1)
    df['value'] = df.apply(lambda x: x['value'], axis=1)

    df = df[[f'{name}', 'date', 'value']]
  
    # Stocker le DataFrame dans un dictionnaire
    return df

df_corn = create_df("corn", "https://www.alphavantage.co/query?function=CORN&interval=monthly", " I1TVUXGTKDYPXB78 ")
df_wheat = create_df("wheat", "https://www.alphavantage.co/query?function=WHEAT&interval=monthly", " I1TVUXGTKDYPXB78 ")
df_sugar = create_df("sugar","https://www.alphavantage.co/query?function=SUGAR&interval=monthly","I1TVUXGTKDYPXB78" )
df_coffee= create_df("coffee", "https://www.alphavantage.co/query?function=COFFEE&interval=monthly", "I1TVUXGTKDYPXB78")
df_index= create_df("index", "https://www.alphavantage.co/query?function=ALL_COMMODITIES&interval=monthly", "I1TVUXGTKDYPXB78")


st.dataframe(df_corn)
st.dataframe(df_wheat)
st.dataframe(df_coffee)
st.dataframe(df_index)


df_coffee.to_csv('df_coffee.csv', index=False)  
df_sugar.to_csv('df_sugar.csv', index=False)  
df_corn.to_csv('df_corn.csv', index=False)  
df_wheat.to_csv('df_wheat.csv', index=False)  
df_index.to_csv('df_index.csv', index=False)





#____________________________________________________________________________________________________________________________________________


#                            2_Sidebar_Personnalisé_+_Texte_Defilant
#____________________________________________________________________________________________________________________________________________

st.markdown(
    """
    <style>
    /* Applique des styles uniquement aux liens dans la sidebar */
    section[data-testid="stSidebar"] a {
        color: white; /* Texte blanc */
        text-decoration: none; /* Pas de soulignement */
    }
    section[data-testid="stSidebar"] a:hover {
        color: #00FFFF; /* Optionnel : couleur au survol */
    }
    </style>
    """,
    unsafe_allow_html=True
)
hide_st_style="""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""
marquee_html = """
<div style="overflow: hidden; white-space: nowrap; background-color: #000000; padding: 10px; border: 0px solid #ddd;">
    <span style="display: inline-block; font-size: 24px; color: #FFFFFF; font-weight: bold; animation: scroll-left 10s linear infinite;">
       Vision Globale des Marchés des Commodités : Analyse et Décision
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

#____________________________________________________________________________________________________________________________________________

#                                                   3_Video_+_Pages
#____________________________________________________________________________________________________________________________________________

st.components.v1.html(marquee_html, height=50)

#_FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:____________________________________________________________________________________________________________

# Conteneur pour l'image et le texte
with st.container():
    col1, col2 = st.columns([2, 2])
    
    # Image dans la première colonne
    with col1:
        st.video("pages/picture/bourse2.mp4")
    
    # Gestion des "pages" dans la deuxième colonne
    with col2:
        # Création d'un état pour suivre la "page" actuelle
        if "page_number" not in st.session_state:
            st.session_state.page_number = 1

        # Fonction pour changer de page
        def change_page(next_page):
            st.session_state.page_number = next_page

        # Affichage du contenu en fonction de la page

        if st.session_state.page_number == 1:
            st.markdown(
    "<h1 style='font-size:  20px;'>Transformer les Données en Actions : L'Impact des Dashboards sur la Stratégie</h1>",
    unsafe_allow_html=True
)
            st.write("Ce dashboard a pour objectif de fournir une vision complète et détaillée des cours de marché des commodités. Que ce soit pour une analyse à court terme, à long terme ou pour des prévisions futures, cet outil est conçu pour aider à la prise de décision stratégique et à la gestion des risques.")



        elif st.session_state.page_number == 2:
            st.markdown(
        "<h1 style='font-size: 30px;'>1 - Analyse de court terme</h1>",
        unsafe_allow_html=True
    )
    
            st.write("""
        Faire une analyse à court terme sur une période d'un an présente plusieurs avantages stratégiques et opérationnels, 
        en particulier dans des contextes de marchés dynamiques comme celui des commodités.
    """)

            st.markdown("""
        - 📊 **Identification des tendances saisonnières** : Permet d'anticiper les fluctuations des prix en fonction des saisons.
        - ⚡ **Suivi de la volatilité à court terme** : Permet de réagir rapidement aux fluctuations du marché.
        - 💡 **Optimisation des décisions d'achat et de vente** : Aide à maximiser les gains en achetant quand les prix sont bas et en vendant quand ils sont élevés.
        - 🔮 **Prévision des prix futurs** : Fournit une estimation des évolutions futures des prix des commodités.
        - 📅 **Amélioration de la planification financière** : Aide à prévoir les coûts et les revenus pour l'année à venir.
    """)
       
       
        elif st.session_state.page_number == 3:
           
          st.markdown(
        "<h1 style='font-size: 30px;'>2 - Analyse à long terme</h1>",
        unsafe_allow_html=True
    )
    
          st.write("""
        Faire une analyse à long terme sur plusieurs années permet de comprendre les tendances durables des commodités et d'identifier des opportunités stratégiques à long terme.
    """)

          st.markdown("""
        - 🔄 **Identification des tendances structurelles** : Permet de comprendre les cycles de marché à long terme et d'anticiper les évolutions majeures.
        - 🌍 **Impact des facteurs externes** : Permet de prendre en compte les évolutions géopolitiques, économiques, et sociales qui affectent les prix sur plusieurs années.
        - 📊 **Évaluation des performances économiques** : Analyse la rentabilité et les bénéfices sur le long terme pour évaluer les décisions stratégiques.
        - 🛠️ **Ajustements des stratégies d'approvisionnement** : Aide à planifier les achats et les investissements à long terme pour maximiser les marges.
        - 📅 **Prévisions sur plusieurs années** : Offre une perspective à long terme des tendances de prix, permettant une planification à plus grande échelle.
    """)

#____________________________________________________________________________________________________________________________________________

#                                                   4_CSS_Bouton
#____________________________________________________________________________________________________________________________________________

          st.markdown(
    """
    <style>
    button {
        background-color: #007BFF;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 1.2em;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    button:hover {
        background-color: #007BFF;
        transform: scale(1.05);
    }

    /* Style pour aligner les colonnes */
    .stButton > button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


 # Boutons pour naviguer entre les pages
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.session_state.page_number > 1:
            if st.button("⬅️ Page Précédente"):
                change_page(st.session_state.page_number - 1)

    with col_next:
        if st.session_state.page_number < 3:  # Limite de page pour exemple
            if st.button("Page Suivante ➡️"):
                change_page(st.session_state.page_number + 1)

#FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:


st.sidebar.markdown('[Outils d’Analyse Technique](#outils)', unsafe_allow_html=True)
st.sidebar.markdown('[Méthodes de prévisions](#methodes)', unsafe_allow_html=True)

#____________________________________________________________________________________________________________________________________________

#                                                   5_CSS_+_Cartes
#____________________________________________________________________________________________________________________________________________


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
<div style="overflow: hidden; white-space: nowrap; background-color: #000000; padding: 10px; border: 0px solid #ddd;">
    <span style="display: inline-block; font-size: 24px; color: #FFFFFF; font-weight: bold; animation: scroll-left 10s linear infinite;">
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
#____________________________________________________________________________________________________________________________________________

#                                                   6_Indicateurs
#____________________________________________________________________________________________________________________________________________


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
<div style="overflow: hidden; white-space: nowrap; background-color: #000000; padding: 10px; border: 0px solid #ddd;">
    <span style="display: inline-block; font-size: 24px; color: #FFFFFF; font-weight: bold; animation: scroll-left 10s linear infinite;">
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
        color: #FFFFFF; /* Couleur du texte */
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

#____________________________________________________________________________________________________________________________________________

#                                                   7_Methodes_D'Analyse
#____________________________________________________________________________________________________________________________________________


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

#____________________________________________________________________________________________________________________________________________
