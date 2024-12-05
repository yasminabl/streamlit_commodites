import requests #68S617QRYKZHX4ZN #I1TVUXGTKDYPXB78
import pandas as pd
import streamlit as st 
import plotly 
import numpy as np
import plotly.graph_objects as go
import altair as alt
import plotly.express as px
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from features.functions import *

#____________________________________________Import_données_+_variables __________________________________________________________

df_wheat = pd.read_csv("df_wheat.csv", index_col=None)
df_corn = pd.read_csv("df_corn.csv", index_col=None)
df_coffee = pd.read_csv("df_coffee.csv", index_col=None)
df_index = pd.read_csv("df_index.csv", index_col=None)
df_sugar = pd.read_csv("df_sugar.csv", index_col=None)

#_______________________________________________Nettoyage des doonées________________________________________________

df_index = clean_df(df_index,'index')
df_coffee = clean_df(df_coffee,'coffee')
df_sugar = clean_df(df_sugar,'sugar')
df_corn = clean_df(df_corn,'corn')
df_wheat = clean_df(df_wheat,'wheat')

#_______________________________________________________Fusion_+_Indicateurs_______________________________________________

df_all = pd.concat([df_coffee, df_sugar, df_corn, df_wheat, df_index], axis=1)
df_all_ind = df_all.copy()

df_ind(df_all_ind, 'coffee')
df_ind(df_all_ind, 'corn')
df_ind(df_all_ind, 'sugar')
df_ind(df_all_ind, 'wheat')
df_ind(df_all_ind, 'index')

#_________________________________________________________Selection_periode____________________________________________


df_all_ind_filtered = df_all_ind.iloc[:13,:]
df_all_ind_filtered.index = pd.to_datetime(df_all_ind_filtered.index)


#____________________________________________Sidebar_selection_commodite_+_indicateur____________________________________________


selected_commodities = st.sidebar.multiselect("Sélectionnez les indicateurs à afficher", 
                                    ['coffee','sugar','corn','wheat', 'index'], 
                                    default=['coffee','sugar','corn','wheat', 'index'])

selected_indicators = st.sidebar.multiselect("Sélectionnez les indicateurs à afficher", 
                                    ['MM_coffee','MM_sugar','MM_corn','MM_wheat','MM_index', 
                                    'RSI_coffee','RSI_sugar','RSI_corn', 'RSI_wheat','RSI_index',
                                    'Stochastic_coffee',  'Stochastic_sugar', 'Stochastic_corn', 'Stochastic_wheat', 'Stochastic_index'], 
                                    default=['MM_coffee','MM_sugar','MM_corn','MM_wheat','MM_index'])

#_____________________________________________________Construction_graphique_______________________________________________


display_styled_title(
    "Analyse de l'ensemble des commodités à court terme", 
    font_size="20px", 
    font_color="#FFFFFF", 
    underline_color="#FFFF", 
    underline_width="250px", 
    font_family="Playfair Display"
)

fig_commodities = go.Figure()
fig_indicators = go.Figure()
# Ajout des traces pour les commodités sélectionnées
if 'coffee' in selected_commodities:
    fig_commodities.add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['value_coffee'], mode='lines', name='value_coffee'))
if 'MM_coffee' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['MM_20_coffee'], mode='lines', name='MM 20_coffee'))
    fig_commodities.add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['value_coffee'], mode='lines', name='value_coffee'))
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['MM_200_coffee'], mode='lines', name='MM 200_coffee'))
if 'RSI_coffee' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['RSI_coffee'], mode='lines', name='RSI_coffee'))
if 'Stochastic_coffee' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['Stochastic_coffee'], mode='lines', name='Stochastic_coffee'))

if 'sugar' in selected_commodities:
    fig_commodities.add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['value_sugar'], mode='lines', name='value_sugar'))
if 'MM_sugar' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['MM_20_sugar'], mode='lines', name='MM 20_sugar'))
    fig_commodities.add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['value_sugar'], mode='lines', name='value_sugar'))
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['MM_200_sugar'], mode='lines', name='MM 200_sugar'))
if 'RSI_sugar' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['RSI_sugar'], mode='lines', name='RSI_sugar'))
if 'Stochastic_sugar' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['Stochastic_sugar'], mode='lines', name='Stochastic_sugar'))

if 'corn' in selected_commodities:
    fig_commodities.add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['value_corn'], mode='lines', name='value_corn'))
if 'MM_corn' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['MM_20_corn'], mode='lines', name='MM 20_corn'))
    fig_commodities.add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['value_corn'], mode='lines', name='value_corn'))
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['MM_200_corn'], mode='lines', name='MM 200_corn'))
if 'RSI_corn' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['RSI_corn'], mode='lines', name='RSI_corn'))
if 'Stochastic_corn' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['Stochastic_corn'], mode='lines', name='Stochastic_corn'))

if 'wheat' in selected_commodities:
    fig_commodities.add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['value_wheat'], mode='lines', name='value_wheat'))
if 'MM_wheat' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['MM_20_wheat'], mode='lines', name='MM 20_wheat'))
    fig_commodities.add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['value_wheat'], mode='lines', name='value_wheat'))
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['MM_200_wheat'], mode='lines', name='MM 200_wheat'))
if 'RSI_wheat' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['RSI_wheat'], mode='lines', name='RSI_wheat'))
if 'Stochastic_wheat' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['Stochastic_wheat'], mode='lines', name='Stochastic_wheat'))

if 'index' in selected_commodities:
    fig_commodities.add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['value_index'], mode='lines', name='value_index'))
if 'MM_index' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['MM_20_index'], mode='lines', name='MM 20_index'))
    fig_commodities.add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['value_index'], mode='lines', name='value_index'))
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['MM_200_index'], mode='lines', name='MM 200_index'))
if 'RSI_index' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['RSI_index'], mode='lines', name='RSI_index'))
if 'Stochastic_index' in selected_indicators:
    fig_indicators .add_trace(go.Scatter(x=df_all_ind_filtered.index, y=df_all_ind_filtered['Stochastic_index'], mode='lines', name='Stochastic_index'))

#_______________________________________________________________________________________________________________________

fig_commodities.update_layout(title="Graphique des cours boursier",
                xaxis_title="Date",
                yaxis_title="Valeur du cours ($)",
                legend_title="Indicateurs")

fig_indicators .update_layout(title="Graphique des indicateurs techniques",
                xaxis_title="Date",
                yaxis_title="Valeur du cours ($)",
                legend_title="Indicateurs")

#_____________________________________________________Affichage_streamlit_______________________________________________


# Affichage côte à côte des graphiques
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_commodities)

with col2:
    st.plotly_chart(fig_indicators)


# Liste des commodités
commodities = ["coffee", "sugar", "wheat", "corn", "index"]

# Calcul des rendements mensuels pour chaque commodité
returns_data = {
    commodite: df_all_ind_filtered[f"value_{commodite}"].pct_change().dropna()
    for commodite in commodities
}


# Préparation des données pour le radar chart
radar_data = pd.DataFrame({
    "Commodité": commodities,
    "Volatilité": [df_all_ind_filtered[f"value_{com}"].pct_change().std() for com in commodities],
    "Variation annuelle (%)": [df_all_ind_filtered[f"value_{com}"].pct_change(12).mean() for com in commodities],
    "Prix moyen": [df_all_ind_filtered[f"value_{com}"].mean() for com in commodities]
})

# Création du radar chart en style "toile d'araignée"
fig_radar = px.line_polar(
    radar_data,
    r="Volatilité",  # Indicateur à comparer
    theta="Commodité",
    line_close=True,
    title="Comparaison des indicateurs",
    template="plotly_dark"
)

# Affichage côte à côte des graphiques
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_radar, use_container_width=True)


# Afficher le radar chart et ajouter un texte explicatif sur la volatilité
with col2:
    # Ajouter une analyse sous forme de carte
    st.markdown("""
    <div style="border: 2px solid white; border-radius: 15px; padding: 15px; background-color: #1E1E1E; color: white;">
        <h3 style="text-align: center;">Importance de la Volatilité</h3>
        <p style="font-size: 14px; line-height: 1.6;">
            La volatilité est un indicateur clé pour évaluer les risques associés à une commodité. Elle mesure 
            les fluctuations des prix sur une période donnée et reflète l'incertitude sur le marché. 
            Voici pourquoi elle est importante :
        </p>
        <ul>
            <li><b>Gestion des risques :</b> Une volatilité élevée peut signaler un risque plus grand, mais aussi des opportunités de profit.</li>
            <li><b>Prévisions :</b> Comprendre la volatilité aide à anticiper les tendances et à adapter les stratégies d'investissement.</li>
            <li><b>Comparaison :</b> En comparant la volatilité des commodités, il est possible d'identifier celles qui sont les plus stables ou les plus dynamiques.</li>
        </ul>
        <p style="font-size: 14px;">Ce graphique offre une vue d’ensemble de la volatilité relative des différentes commodités, permettant une analyse approfondie.</p>
    </div>
    """, unsafe_allow_html=True)
    

#_______________________________________________________________________________________________________________________


# Création d'un DataFrame pour les rendements
returns_df = pd.DataFrame(returns_data)

# Création de la boîte à moustaches
fig_boxplot = px.box(
    returns_df,
    title="Distribution des rendements mensuels",
    labels={"value": "Rendements (%)", "variable": "Commodité"},
    template="plotly_white",
)

# Calcul de la matrice de corrélation
corr_matrix = df_all_ind_filtered[[f"value_{commodite}" for commodite in commodities]].corr()

# Création de la heatmap
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Corrélations entre les commodités")

# Affichage des deux graphiques côte à côte
col1, col2 = st.columns(2)

# Afficher la boîte à moustaches dans la première colonne
with col1:
    st.plotly_chart(fig_boxplot, use_container_width=True)

# Afficher la heatmap dans la deuxième colonne
with col2:
    st.pyplot(fig)
