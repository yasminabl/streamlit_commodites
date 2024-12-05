import requests #68S617QRYKZHX4ZN #I1TVUXGTKDYPXB78
import pandas as pd
import streamlit as st 
import plotly 
import numpy as np
import plotly.graph_objects as go
import altair as alt
import plotly.express as px
from datetime import datetime
from functions import *
from PIL import Image
import base64


df_wheat = pd.read_csv("df_wheat.csv",index_col=None)
df_corn = pd.read_csv("df_corn.csv",index_col=None)
df_coffee = pd.read_csv("df_coffee.csv",index_col=None)
df_index = pd.read_csv("df_index.csv",index_col=None)
df_sugar = pd.read_csv("df_sugar.csv",index_col=None)

df_coffee = process_dataframe(df_coffee, 'coffee')
df_coffee = drop_unnamed_columns(df_coffee)
df_coffee_2 = df_coffee.copy()

 #__________________________________________TITRE ET IMAGE___________________________________________________________


image_path = "/Users/paultournaire/Desktop/Master/M2/Streamlit/PROJET/pages/picture/coffee.jpeg" 
image_base64 = get_image_base64(image_path) 

# Ajoute l'image et le titre avec HTML et CSS
st.markdown(f"""
    <div class="header-container">
        <div class="image-container">
            <img src="data:image/png;base64,{image_base64}" alt="Café" class="centered-image">
        </div>
        <div class="text-container">
            <h1 class="main-title">Café : l’or brun sous la loupe des investisseurs</h1>
            <div class="line"></div>
            <p class="main-subtitle">Analyse approfondie des tendances, performances et métriques clés du marché du café</p>
        </div>
    </div>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
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
            font-family: 'Poppins', sans-serif;
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
            color: #bbbbbb; /* Gris clair */
            margin: 0;
        }
    </style>
""", unsafe_allow_html=True)


#_____________________________________________________BARRE DEFILANTE_________________________________________________

# Conversion de l'index en datetime si nécessaire
df_coffee_2.index = pd.to_datetime(df_coffee.index, errors='coerce')

# Calcul du taux de fermeture mensuel en prenant la dernière valeur

df_coffee_monthly = df_coffee_2.resample('M').last()

# Calcul du pourcentage de variation par rapport à l'année précédente
df_coffee_monthly['Taux_Fermeture'] = df_coffee_monthly['value_coffee']
df_coffee_monthly['Variation_%'] = df_coffee_monthly['Taux_Fermeture'].pct_change(12) * 100

# Calcul de la volatilité mensuelle
volatility_monthly = df_coffee_monthly['Taux_Fermeture'].pct_change().std()
volatility_monthly_display = f"{volatility_monthly:.2f}%"

# Valeurs actuelles pour la carte (vérification de valeurs non manquantes)
current_rate = df_coffee_monthly['Taux_Fermeture'].iloc[-1] if not df_coffee_monthly['Taux_Fermeture'].empty else np.nan
previous_year_rate = df_coffee_monthly['Taux_Fermeture'].shift(12).iloc[-1] if not df_coffee_monthly['Taux_Fermeture'].shift(12).empty else np.nan

# Calcul du changement en pourcentage
percentage_change = ((current_rate - previous_year_rate) / previous_year_rate * 100) if previous_year_rate else np.nan
current_rate_display = f"{current_rate:.2f}$" if not np.isnan(current_rate) else "N/A"
percentage_change_display = f"{percentage_change:.2f}% vs LY" if not np.isnan(percentage_change) else "N/A"

# Détermine l'icône de flèche selon la variation
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

# CSS pour la carte et la barre défilante
st.markdown(f"""
    <style>
    .barre-defilante {{
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        display: flex;
        animation: defilement 15s linear infinite;
    }}
    .barre-defilante span {{
        display: inline-block;
        margin: 0 20px;
    }}
    .rate-value {{
        font-size: 16px;
        font-weight: bold;
    }}
    .rate-change {{
        font-size: 14px;
    }}
    @keyframes defilement {{
        0% {{ transform: translateX(100%); }}
        100% {{ transform: translateX(-100%); }}
    }}
    </style>
    """, unsafe_allow_html=True)


trend = "Haussiere" if (df_coffee_monthly['Taux_Fermeture'].diff() > 0).iloc[-3:].all() else "Baissiere"
tendance_display = trend
# Détermine la couleur en fonction de la tendance
if trend == "Haussiere":
    trend_style = "color: green;"  # Texte en vert
elif trend == "Baissiere":
    trend_style = "color: red;"  # Texte en rouge
else:
    trend_style = "color: gray;"  # Texte en gris neutre

# Détermine la performance et sa couleur
performance = (
    "Stable" if volatility_monthly < 0.02 else 
    "Volatil" if 0.02 <= volatility_monthly < 0.05 else 
    "Très volatil"
)
performance_display = f"{performance}"

if performance == "Stable":
    performance_style = "color: green;"  # Texte en vert
elif performance == "Volatil":
    performance_style = "color: orange;"  # Texte en orange
elif performance == "Très volatil":
    performance_style = "color: darkred;"  # Texte en rouge
else:
    performance_style = "color: gray;"  # Texte en gris neutre

# Contenu HTML de la barre défilante avec performance et tendance
contenu = f"""
<span>
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

# Affichage de la barre défilante dans Streamlit
st.markdown(contenu, unsafe_allow_html=True)

# CODE POUR LES ICONES
st.markdown("""
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
""", unsafe_allow_html=True)

#_______________________________________________________GRAPHIQUE DES DONNEES_______________________________________________
col1, col2 = st.columns([2, 3])
with col1 :
    st.subheader("Valeurs boursières quotidiennes du mais")

    st.dataframe(df_coffee)


with col2 :
    st.subheader("Données descriptive sur le mais")
    st.dataframe(df_coffee.describe())

df_index = process_dataframe(df_index, 'index')
df_index = drop_unnamed_columns(df_index)
#df_index.index = pd.to_datetime(df_index.index, errors='coerce')

sub_df_coffee = pd.concat([df_coffee, df_index], axis =1)
sub_df_coffee_ind = sub_df_coffee.copy()

#_______________________________________________________________________________________________________________________

sub_df_coffee_ind['MM_20'] = sub_df_coffee_ind['value_coffee'].iloc[::-1].rolling(window=20).mean().iloc[::-1]
sub_df_coffee_ind['MM_200'] = sub_df_coffee_ind['value_coffee'].iloc[::-1].rolling(window=200).mean().iloc[::-1]
sub_df_coffee_ind['RSI'] = compute_rsi(sub_df_coffee_ind['value_coffee'])
sub_df_coffee_ind['Stochastic'] = compute_stochastics(sub_df_coffee_ind['value_coffee'])

#_______________________________________________________________________________________________________________________


sub_df_coffee.index = pd.to_datetime(sub_df_coffee.index)
sub_df_coffee_ind.index = pd.to_datetime(sub_df_coffee.index)

years = sub_df_coffee.index.year.unique()
months = range(1, 13)  
last_month = sub_df_coffee.index[-1].month 
current_month = sub_df_coffee.index[0].month 

selected_year_min = st.sidebar.selectbox("Sélectionnez l'année de départ", options=years, index=len(years) - 1)
selected_month_min = st.sidebar.selectbox("Sélectionnez le mois de départ", options=months, index=list(months).index(last_month))

selected_year_max = st.sidebar.selectbox("Sélectionnez l'année de fin", options=years, index=0)
selected_month_max = st.sidebar.selectbox("Sélectionnez le mois de fin", options=months, index=list(months).index(current_month))

start_date = pd.Timestamp(year=selected_year_min, month=selected_month_min, day=1)
end_date = pd.Timestamp(year=selected_year_max, month=selected_month_max, day=1) + pd.offsets.MonthEnd(1)

sub_df_coffee_filtered = sub_df_coffee[(sub_df_coffee.index >= pd.to_datetime(start_date)) & 
                            (sub_df_coffee.index <= pd.to_datetime(end_date))]

sub_df_coffee_ind_filtered = sub_df_coffee_ind[(sub_df_coffee.index >= pd.to_datetime(start_date)) & 
                            (sub_df_coffee_ind.index <= pd.to_datetime(end_date))]

#_______________________________________________________________________________________________________________________
selected_commodities = st.sidebar.radio("Sélectionnez les commodités à afficher", 
                                        ["Coffee", "Index", "Les deux"], 
                                        index=2)  # L'index 2 sélectionne "Les deux" par défaut

# Logique pour ajuster les colonnes à afficher en fonction de la sélection
if selected_commodities == "Coffee":
    columns_to_display = ['value_coffee']
elif selected_commodities == "Index":
    columns_to_display = ['value_index']
else:  # "Les deux"
    columns_to_display = ['value_coffee', 'value_index']

st.subheader(f"Graphique des {selected_commodities}")
st.line_chart(sub_df_coffee_ind_filtered[columns_to_display])
#_______________________________________________________________________________________________________________________

#_______________________________________________________________________________________________________________________

selected_indicators = st.sidebar.radio("Sélectionnez les indicateurs à afficher", 
                                    [ 'MM', 'RSI', 'Stochastic'])


# Création du graphique avec Plotly
fig = go.Figure()

# Ajout des traces pour les commodités sélectionnées
if 'MM' in selected_indicators:
    fig.add_trace(go.Scatter(x=sub_df_coffee_ind_filtered.index, y=sub_df_coffee_ind_filtered['MM_20'], mode='lines', name='MM 20'))
    fig.add_trace(go.Scatter(x=sub_df_coffee_ind_filtered.index, y=sub_df_coffee_ind_filtered['MM_200'], mode='lines', name='MM 200'))
if 'RSI' in selected_indicators:
    fig.add_trace(go.Scatter(x=sub_df_coffee_ind_filtered.index, y=sub_df_coffee_ind_filtered['RSI'], mode='lines', name='RSI'))
if 'Stochastic' in selected_indicators:
    fig.add_trace(go.Scatter(x=sub_df_coffee_ind_filtered.index, y=sub_df_coffee_ind_filtered['Stochastic'], mode='lines', name='Stochastic'))

# Mise en forme du graphique
fig.update_layout(title="Graphique des indicateurs techniques",
                xaxis_title="Date",
                yaxis_title="Valeur",
                legend_title="Indicateurs")

# Affichage du graphique dans Streamlit
st.plotly_chart(fig)
#______________________________________________________________________________________________________________________ffee