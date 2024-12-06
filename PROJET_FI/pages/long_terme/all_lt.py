import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from features.functions import *
from features.layout import *

'''
Sommaire : 

1_Import_Données_+_Définition_Vriables
2_Nettoyage_Données
3_Titre_+_Image
4_Fusion_Tableaux+_Ajout_Indicateurs
5_Séléction_Période
6_Sidebar_Séléction_Commodite_&_Indicateur
7_Construction_graphique
8_Affichage_Streamlit
9_Radar_Chart_&_Analyse_Volatilité
10_Box_Plot_&_Heatmap

'''

#____________________________________________________________________________________________________________________________________________

#                                                   1_Import_Données_+_Définition_Vriables
#____________________________________________________________________________________________________________________________________________

df_wheat = pd.read_csv("df_wheat.csv", index_col=None)
df_corn = pd.read_csv("df_corn.csv", index_col=None)
df_coffee = pd.read_csv("df_coffee.csv", index_col=None)
df_index = pd.read_csv("df_index.csv", index_col=None)
df_sugar = pd.read_csv("df_sugar.csv", index_col=None)

#____________________________________________________________________________________________________________________________________________

#                                                   2_Nettoyage_Données
#____________________________________________________________________________________________________________________________________________

df_index = clean_df(df_index,'index')
df_coffee = clean_df(df_coffee,'coffee')
df_sugar = clean_df(df_sugar,'sugar')
df_corn = clean_df(df_corn,'corn')
df_wheat = clean_df(df_wheat,'wheat')

#____________________________________________________________________________________________________________________________________________

#                                                   3_Titre_+_Image
#____________________________________________________________________________________________________________________________________________

display_styled_title(
    "Analyse de l'ensemble des commodités à long terme", 
    font_size="20px", 
    font_color="#FFFFFF", 
    underline_color="#FFFF", 
    underline_width="250px", 
    font_family="Playfair Display"
)

#____________________________________________________________________________________________________________________________________________

#                                                   4_Fusion_Tableaux+_Ajout_Indicateurs
#____________________________________________________________________________________________________________________________________________

df_all = pd.concat([df_coffee, df_sugar, df_corn, df_wheat, df_index], axis=1)
df_all_ind = df_all.copy()

df_ind(df_all_ind, 'coffee')
df_ind(df_all_ind, 'corn')
df_ind(df_all_ind, 'sugar')
df_ind(df_all_ind, 'wheat')
df_ind(df_all_ind, 'index')

#____________________________________________________________________________________________________________________________________________

#                                                   5_Séléction_Période
#____________________________________________________________________________________________________________________________________________

df_all_ind.index = pd.to_datetime(df_all_ind.index)

selected_year_min, selected_month_min, selected_year_max, selected_month_max = get_date_range_from_sidebar(df_all_ind)

df_all_ind_filtered = filter_dataframe(df_all_ind, 
                                              selected_year_min, selected_month_min, 
                                              selected_year_max, selected_month_max)


df_all_ind_filtered.index = pd.to_datetime(df_all_ind_filtered.index)

#____________________________________________________________________________________________________________________________________________

#                                                   6_Sidebar_Séléction_Commodite_&_Indicateur
#____________________________________________________________________________________________________________________________________________

selected_commodities = st.sidebar.multiselect("Sélectionnez les indicateurs à afficher", 
                                    ['coffee','sugar','corn','wheat', 'index'], 
                                    default=['coffee','sugar','corn','wheat', 'index'])

selected_indicators = st.sidebar.multiselect("Sélectionnez les indicateurs à afficher", 
                                    ['MM_coffee','MM_sugar','MM_corn','MM_wheat','MM_index', 
                                    'RSI_coffee','RSI_sugar','RSI_corn', 'RSI_wheat','RSI_index',
                                    'Stochastic_coffee',  'Stochastic_sugar', 'Stochastic_corn', 'Stochastic_wheat', 'Stochastic_index'], 
                                    default=['MM_coffee','MM_sugar','MM_corn','MM_wheat','MM_index'])

#____________________________________________________________________________________________________________________________________________

#                                                   7_Construction_graphique
#____________________________________________________________________________________________________________________________________________

fig_commodities = go.Figure()


# Définir les commodités
commodities = ["coffee", "sugar", "wheat", "corn", "index"]

# Vérifiez que dfs contient les DataFrames pour chaque commodité
dfs = {
    "coffee": df_coffee,
    "sugar": df_sugar,
    "wheat": df_wheat,
    "corn": df_corn,
    "index": df_index
}

# Assurez-vous que l'index de chaque DataFrame est en datetime et les longueurs sont alignées
for commodite in commodities:
    # Convertir l'index en datetime
    dfs[commodite].index = pd.to_datetime(dfs[commodite].index, errors='coerce')

    # Vérifier la longueur et résoudre les désalignements
    if len(dfs[commodite][f"value_{commodite}"]) != len(dfs[commodite].index):
        dfs[commodite] = dfs[commodite].dropna()  # Supprimer les lignes avec des données manquantes ou désalignées

# Tracer les cours boursiers des commodités
fig = go.Figure()
for commodite in commodities:
    fig.add_trace(go.Scatter(
        x=dfs[commodite].index,
        y=dfs[commodite][f"value_{commodite}"],
        mode='lines',
        name=commodite.capitalize()
    ))

fig.update_layout(
    title="Comparaison des cours boursiers",
    xaxis_title="Date",
    yaxis_title="Valeur ($)",
    legend_title="Commodités",
    template="plotly_white"
)


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

fig_commodities.update_layout(title="<u>Graphique des cours boursier</u>",
                xaxis_title="Date",
                yaxis_title="Valeur du cours ($)",
                legend_title="Indicateurs")

fig_indicators .update_layout(title="<u>Graphique des indicateurs techniques</u>",
                xaxis_title="Date",
                yaxis_title="Valeur du cours ($)",
                legend_title="Indicateurs")

#____________________________________________________________________________________________________________________________________________

#                                                   8_Affichage_Streamlit
#____________________________________________________________________________________________________________________________________________

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
    title="<u>Comparaison des indicateurs</u>",
    template="plotly_dark"
)
#____________________________________________________________________________________________________________________________________________

#                                                   9_Radar_Chart_&_Analyse_Volatilité
#____________________________________________________________________________________________________________________________________________

commodities = ["coffee", "sugar", "wheat", "corn", "index"]
radar_data = pd.DataFrame({
    "Commodité": commodities,
    "Volatilité": [df_all_ind_filtered[f"value_{com}"].pct_change().std() for com in commodities],
    "Variation annuelle (%)": [df_all_ind_filtered[f"value_{com}"].pct_change(12).mean() for com in commodities],
    "Prix moyen": [df_all_ind_filtered[f"value_{com}"].mean() for com in commodities]
})

fig_radar = px.line_polar(
    radar_data,
    r="Volatilité",
    theta="Commodité",
    line_close=True,
    title="<u>Comparaison des Indicateurs</u>",
    template="plotly_dark"
)

# Radar chart and explanation
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_radar, use_container_width=True)

with col2:
    st.markdown("""
    <div style="border: 2px solid white; border-radius: 15px; padding: 15px; background-color: #1E1E1E; color: white;">
        <h3 style="text-align: center;">Importance de la Volatilité</h3>
        <p>La volatilité est essentielle pour comprendre les risques et les opportunités sur les marchés des commodités.</p>
        <ul>
            <li><b>Gestion des Risques:</b> Une volatilité élevée signale des risques mais aussi des opportunités.</li>
            <li><b>Prévisions:</b> Elle aide à anticiper les fluctuations futures.</li>
            <li><b>Comparaison:</b> Permet d'évaluer la stabilité relative des commodités.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

#____________________________________________________________________________________________________________________________________________

#                                                   10_Box_Plot_&_Heatmap
#____________________________________________________________________________________________________________________________________________

returns_data = {com: df_all_ind_filtered[f"value_{com}"].pct_change().dropna() for com in commodities}
returns_df = pd.DataFrame(returns_data)

fig_boxplot = px.box(
    returns_df,
    title="<u>Distribution des Rendements Mensuels</u>",
    labels={"value": "Rendements (%)", "variable": "Commodité"},
    template="plotly_white"
)

# Correlation matrix
corr_matrix = df_all_ind_filtered[[f"value_{com}" for com in commodities]].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Corrélations entre les Commodités")

# Display side-by-side
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_boxplot, use_container_width=True)

with col2:
    st.pyplot(fig)

#____________________________________________________________________________________________________________________________________________
