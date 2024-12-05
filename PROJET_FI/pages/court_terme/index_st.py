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
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

'''
Sommaire : 

1_Import_Données_+_Définition_Vriables
2_Nettoyage_Données
3_Titre_+_Image
4_Fusion_Tableaux+_Ajout_Indicateurs
5_Séléction_Période
6_Sidebar_Séléction_Commodite_&_Indicateur
7_Affichage_Streamlit

'''
#____________________________________________________________________________________________________________________________________________

#                                                   1_Import_Données_+_Définition_Variables
#____________________________________________________________________________________________________________________________________________

commodite = 'index'
unique_id = 'st'
df_index = pd.read_csv("df_index.csv",index_col=None)

#____________________________________________________________________________________________________________________________________________

#                                                   2_Nettoyage_Données
#____________________________________________________________________________________________________________________________________________

df_index = process_dataframe(df_index, 'index')
df_index = drop_unnamed_columns(df_index)
df_index_2 = df_index.copy()

#____________________________________________________________________________________________________________________________________________

#                                                   3_Titre_+_Image
#____________________________________________________________________________________________________________________________________________

picture = get_picture(commodite)
title = "L'Index : Le Thermomètre Global des Marchés"
subtitle = "Plongez dans les tendances et performances qui définissent l'équilibre des commodités."
display_header(picture, title, subtitle)
display_bar(df_index_2, commodite)
reverse_dataframe(df_index)

#____________________________________________________________________________________________________________________________________________

#                                                   4_Fusion_Tableaux+_Ajout_Indicateurs
#____________________________________________________________________________________________________________________________________________

sub_df_index_ind = df_index.copy()
df_ind(sub_df_index_ind, commodite)

#____________________________________________________________________________________________________________________________________________

#                                                   5_Séléction_Période
#____________________________________________________________________________________________________________________________________________

df_index_ind_filtered = sub_df_index_ind.iloc[:13,:]

#____________________________________________________________________________________________________________________________________________

#                                                   6_Sidebar_Séléction_Commodite_&_Indicateur
#____________________________________________________________________________________________________________________________________________
 
selected_commodity = st.sidebar.radio("Sélectionnez les cours à afficher", 
                                    [ commodite],
                                    index=0)

selected_indicators = st.sidebar.radio("Sélectionnez les indicateurs à afficher", 
                                    [ f'MM_{commodite}', f'RSI_{commodite}', f'Stochastic_{commodite}'])

#____________________________________________________________________________________________________________________________________________

#                                                   7_Affichage_Streamlit
#____________________________________________________________________________________________________________________________________________

display_custom_table(df_index_2.iloc[:13,:], "Données descriptives sur l'index")

col1, col2, col3 = st.columns(3)

# Graphique 1 : Cours Boursiers
with col1:
   
    fig1, title1 = graph_cours_boursier(df_index_ind_filtered, selected_commodity, commodite)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 10px;">
            <span style="font-size: 16px; font-weight: bold; text-decoration: underline; color: #FFFFFF;">
                {title1}
            </span>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Graphique 2 : Indicateurs Techniques
with col2:
   
    fig2 = graph_indicateurs(df_index_ind_filtered, commodite, selected_indicators)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown(
        """
        <div style="text-align: center; margin-top: 10px;">
            <span style="font-size: 16px; font-weight: bold; text-decoration: underline; color: #FFFFFF;">
                Graphique des indicateurs techniques
            </span>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Texte explicatif dans la troisième colonne
with col3:
    st.markdown(
        """
        <div style="border: 2px solid white; border-radius: 10px; padding: 15px; background-color: #000000; color: white;">
            <h3 style="color: white; text-align: center;">Faits en bref</h3>
            <p style="text-align: justify;">
Attention : le réchauffement climatique, un enjeu de plus en plus préoccupant.            </p>
            <p style="text-align: justify;">
              Le réchauffement climatique joue un rôle clé dans la volatilité des prix agricoles, notamment pour le maïs. Les conditions météorologiques extrêmes, telles que les sécheresses ou les pluies excessives, perturbent les cycles de semis et de récolte, réduisant les rendements. Une offre plus incertaine ou diminuée face à une demande stable ou croissante entraîne des hausses de prix. Par ailleurs, les événements climatiques peuvent aussi entraîner des coûts supplémentaires pour les producteurs, comme l'irrigation ou des stratégies d'adaptation, qui se répercutent sur les prix finaux. Cette instabilité rend le marché plus imprévisible, attirant parfois la spéculation, ce qui accentue encore davantage les fluctuations des prix.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

graph_cours_boursier(df_index_ind_filtered,selected_commodity, commodite)
graph_indicateurs(df_index_ind_filtered, commodite, selected_indicators)
#______________________________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________

# Nettoyage des données
# Remplacez les NaN et les chaînes vides par des valeurs par défaut
all_data = all_data.replace('', float('nan'))  # Convertir les chaînes vides en NaN
all_data = all_data.dropna()  # Supprimer les lignes contenant des NaN

# Préparation des données
scaled_data = StandardScaler().fit_transform(all_data)

# Clustering
kmeans = KMeans(n_clusters=3, random_state=0).fit(scaled_data)
all_data['Cluster'] = kmeans.labels_  # Ajouter les clusters au DataFrame

# Visualisation
fig = px.scatter(
    all_data,
    x=all_data.index,  # Remplacez par la colonne souhaitée si nécessaire
    y="index",  # Nom de la colonne à afficher sur l'axe Y
    color="Cluster",
    title="Clustering des commodités",
    color_continuous_scale=px.colors.qualitative.Set1,
)
st.plotly_chart(fig)

#____________________________________________________________________________________________________________________________________________

