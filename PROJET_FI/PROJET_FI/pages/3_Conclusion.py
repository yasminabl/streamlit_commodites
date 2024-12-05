
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
import os 



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


df_coffee_hw = df_coffee.copy()
df_sugar_hw = df_sugar.copy()
df_corn_hw = df_corn.copy()
df_wheat_hw = df_wheat.copy()
df_index_hw = df_index.copy()


df_dict_hw = {
    'coffee': df_coffee_hw,
    'sugar': df_sugar_hw,
    'corn': df_corn_hw,
    'wheat': df_wheat_hw,
    'index': df_index_hw
}


st.header('Prévision pour les prochains mois')
forecast_horizon = st.sidebar.number_input(
    'Entrez le nombre de mois à prévoir:', 
    min_value=1,  # Valeur minimale de 1 mois
    max_value=24,  # Valeur maximale de 12 mois
    value=12,  # Valeur par défaut
    step=1  # Incrément de 1 pour chaque pas
)

st.header('Choix des paramètres')
alpha = st.sidebar.number_input(
    'Choisissez la valeur alpha :', 
    min_value=0.0,  # Valeur minimale de 1 mois
    max_value=1.0,  # Valeur maximale de 12 mois
    value=0.1,  # Valeur par défaut
    step=0.1  # Incrément de 1 pour chaque pas
)

beta = st.sidebar.number_input(
    'Choisissez la valeur beta :', 
    min_value=0.0,  # Valeur minimale de 1 mois
    max_value=1.0,  # Valeur maximale de 12 mois
    value=0.1,  # Valeur par défaut
    step=0.1  # Incrément de 1 pour chaque pas
)

gamma = st.sidebar.number_input(
    'Choisissez la valeur gamma :', 
    min_value=0.0,  # Valeur minimale de 1 mois
    max_value=1.0,  # Valeur maximale de 12 mois
    value=0.1,  # Valeur par défaut
    step=0.1  # Incrément de 1 pour chaque pas
)

season_length = st.sidebar.number_input(
    'Choisissez la saisonnalité :', 
    min_value=1,  # Valeur minimale de 1 mois
    max_value=12,  # Valeur maximale de 12 mois
    value=12,  # Valeur par défaut
    step=1 # Incrément de 1 pour chaque pas
)
#_______________________________________________________Fusion_+_Indicateurs_______________________________________________

df_all = pd.concat([df_coffee, df_sugar, df_corn, df_wheat, df_index], axis=1)
df_all_ind = df_all.copy()

df_ind(df_all_ind, 'coffee')
df_ind(df_all_ind, 'corn')
df_ind(df_all_ind, 'sugar')
df_ind(df_all_ind, 'wheat')
df_ind(df_all_ind, 'index')


#_______________________________________________________________________________________________________________________
date = df_all.index[0]

df_forecast = generate_hw_forecasts(df_dict_hw, forecast_horizon, alpha, beta, gamma, season_length)

# Générer les conclusions avec les prévisions ajoutées
df_conclusion = generate_conclusion(df_all_ind, date, df_forecast)

# Afficher la conclusion
st.dataframe(df_conclusion)

#_______________________________________________________________________________________________________________________



#_______________________________________________________________________________________________________________________

#_______________________________________________________________________________________________________________________

#_______________________________________________________________________________________________________________________

#_______________________________________________________________________________________________________________________

