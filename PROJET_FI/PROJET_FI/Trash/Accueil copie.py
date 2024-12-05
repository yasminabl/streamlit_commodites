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
from functions import *


#_______________________________________________________________________________________________________________________
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
#_______________________________________________________________________________________________________________________


st.sidebar.markdown('[Objectif](#objectif)', unsafe_allow_html=True)
st.sidebar.markdown('[Définition des Soft Commodities](#definition)', unsafe_allow_html=True)
st.sidebar.markdown('[Outils d’Analyse Technique](#outils)', unsafe_allow_html=True)
st.sidebar.markdown('[Méthodes de prévisions](#methodes)', unsafe_allow_html=True)

#_______________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________

st.header("Dashboard d'aide à la prise de décision sur les commodités")

st.subheader("Présenté par Yasmina BELLIL & Paul TOURNAIRE ")

add_anchor("objectif")
st.subheader("")
st.subheader('Objectif : Comment un Dashboard aide à la prise de décision')
st.write("Un dashboard est un outil puissant qui permet de visualiser des données complexes de manière claire et concise, facilitant ainsi la prise de décision. En intégrant diverses sources de données et en les présentant sous forme de graphiques interactifs et de tableaux, un dashboard permet aux utilisateurs d’analyser rapidement les performances, les tendances et les risques associés à un ensemble d’indicateurs clés. Dans le contexte des commodités, un dashboard peut fournir une vue d’ensemble en temps réel des prix, des fluctuations et des indicateurs techniques, permettant ainsi aux investisseurs et aux gestionnaires de portefeuille de prendre des décisions éclairées. L’accessibilité immédiate des informations critiques aide à anticiper les évolutions du marché, à identifier des opportunités et à limiter les risques en réagissant de manière proactive.")

add_anchor("definition")
st.subheader("")
st.subheader('Définition des Soft Commodities : Café, Sucre, Maïs et Blé')

st.markdown("""
Les **soft commodities** font référence à des matières premières agricoles qui sont cultivées et récoltées, contrairement aux hard commodities telles que les métaux et l’énergie. Parmi les soft commodities les plus importantes, on trouve :

- **Café** : Le café est l'une des boissons les plus consommées au monde et une commodité essentielle sur les marchés mondiaux. Il est principalement cultivé dans les régions tropicales, avec des producteurs majeurs tels que le Brésil, le Vietnam et la Colombie. Le prix du café est influencé par des facteurs tels que la météo, les récoltes, et les tendances de consommation.

- **Sucre** : Le sucre est un produit de base qui provient principalement de la canne à sucre et de la betterave. Il est un ingrédient clé dans l'industrie alimentaire et est utilisé mondialement. Les prix du sucre peuvent être influencés par des facteurs climatiques, des changements dans les politiques agricoles, et des mouvements de la demande mondiale.

- **Maïs** : Le maïs est l’une des céréales les plus cultivées et utilisées dans le monde, que ce soit pour l’alimentation humaine, animale ou la production de biocarburants. Le maïs est particulièrement sensible aux variations climatiques et aux changements dans les habitudes alimentaires.

- **Blé** : Le blé est une céréale essentielle pour l’alimentation humaine et représente une part importante des récoltes mondiales. Les prix du blé sont affectés par les conditions météorologiques, les rendements des récoltes, et la demande des marchés internationaux.

Ces commodités agricoles sont soumises à des fluctuations fréquentes des prix, influencées par des facteurs économiques, climatiques et politiques. Analyser leur évolution à travers des outils d'analyse technique est crucial pour prendre des décisions de trading ou d'investissement.
""")

add_anchor("outils")
st.subheader("")
st.subheader('Outils d’Analyse Technique : Moyenne Mobile, RSI et Stochastique')

st.markdown("""
Les outils d’analyse technique sont des indicateurs mathématiques utilisés pour prévoir les évolutions futures des prix d’un actif. Voici une définition de trois des indicateurs techniques couramment utilisés pour l'analyse des commodités :

- **Moyenne Mobile (MM)** : La moyenne mobile est un indicateur qui permet de lisser les données de prix sur une période donnée pour en dégager une tendance. Elle est utilisée pour identifier la direction du marché et les niveaux de support et de résistance. Par exemple, une moyenne mobile à 20 jours lisse les prix sur les 20 derniers jours et aide à identifier si le marché est haussier ou baissier. Une croissance de la moyenne mobile signale généralement une tendance haussière, tandis qu'une baisse signale une tendance baissière.

- **RSI (Relative Strength Index)** : Le RSI est un indicateur de momentum qui mesure la vitesse et le changement des mouvements de prix. Il oscille entre 0 et 100 et est utilisé pour déterminer si un actif est suracheté ou survendu. Un RSI supérieur à 70 indique généralement que le marché est suracheté et pourrait être prêt pour une correction, tandis qu’un RSI inférieur à 30 indique que le marché est survendu et pourrait rebondir.

- **Stochastique** : L'indicateur stochastique mesure la relation entre le prix de clôture d'un actif et son range de prix sur une période donnée. Il oscille également entre 0 et 100, et il est utilisé pour identifier des conditions de surachat ou de survente. Un stochastique supérieur à 80 indique une condition de surachat, tandis qu’un stochastique inférieur à 20 indique une condition de survente, suggérant un potentiel retournement de tendance.

Ces indicateurs permettent de comprendre l'état du marché, d’identifier les signaux de renversement ou de continuation des tendances, et d’optimiser les décisions d'achat ou de vente sur les commodités. L’utilisation conjointe de ces outils renforce l’analyse des prix et permet d’obtenir des prévisions plus précises pour la gestion de portefeuilles ou la prise de décisions stratégiques.
""")
                               
add_anchor("methodes")
st.subheader("")
st.subheader('Méthodes de prévisions : Moyenne Mobile, Lissage Exponentiel Simple, Lissage Exponentiel Double, Holt & Winter ')

st.markdown("""

- **Moyenne Mobile (MM)** : La méthode des moyennes mobiles est une technique statistique utilisée pour lisser les séries temporelles et rendre plus visibles les tendances sous-jacentes en éliminant les variations aléatoires. Elle consiste à calculer la moyenne d’un ensemble de données sur une période fixe (par exemple, les 4 derniers mois) et à faire glisser cette fenêtre de moyenne à travers la série temporelle. Cette méthode est particulièrement utile pour des séries sans tendance marquée ou saisonnalité, mais elle peut avoir du mal à capturer des changements rapides dans les données.
            
- **Lissage Exponentiel Simple (LES)** : Le lissage exponentiel simple (ou Simple Exponential Smoothing, SES) est une méthode qui attribue un poids décroissant aux observations passées, ce qui permet de donner plus d'importance aux valeurs récentes de la série temporelle. La prévision pour une période future est une combinaison pondérée des valeurs passées, avec un paramètre alpha (compris entre 0 et 1) qui détermine l'importance des données récentes par rapport aux anciennes. Cette méthode est idéale pour des séries sans tendance ou saisonnalité, mais elle peut ne pas capturer efficacement des structures de données plus complexes.
            
- **Lissage Exponentiel Double (LED)** : Le lissage exponentiel double (ou Double Exponential Smoothing, DES) est une extension du lissage exponentiel simple, conçue pour traiter des séries temporelles qui présentent une tendance. En plus du paramètre alpha pour contrôler le poids des données récentes, cette méthode introduit un paramètre beta pour modéliser la tendance de la série. Ainsi, le lissage exponentiel double permet de prévoir les données en tenant compte à la fois du niveau et de la tendance, ce qui le rend plus adapté aux séries qui montrent des changements à long terme.

- **Holt & Winter)** : Les méthodes de Holt et Winter (ou Holt-Winters) sont des modèles avancés de lissage exponentiel qui permettent de prendre en compte à la fois une tendance et une saisonnalité dans les séries temporelles. La méthode de Holt est une version plus avancée du lissage exponentiel double, qui ajuste à la fois le niveau et la tendance avec deux paramètres, alpha et beta. La méthode de Winter (ou Holt-Winters) ajoute un troisième paramètre, gamma, pour modéliser la saisonnalité. Cela rend cette méthode particulièrement puissante pour les séries présentant des cycles réguliers (par exemple, des ventes saisonnières). Le modèle ajustera ainsi la prévision en fonction des variations saisonnières, en plus de la tendance et du niveau.
""")

