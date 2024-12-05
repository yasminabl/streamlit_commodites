
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
import os 



#____________________________________________________________________________________________________________________________________________

#                                                   1_Import_Données
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


st.header('Conclusion')

forecast_horizon, alpha, beta, gamma, season_length = sidebar_parametres_previsions()

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

#                                                   5_Affichage_Streamlit
#____________________________________________________________________________________________________________________________________________

date = df_all.index[0]

df_forecast = generate_hw_forecasts(df_dict_hw, forecast_horizon, alpha, beta, gamma, season_length)

# Générer les conclusions avec les prévisions ajoutées
df_conclusion = generate_conclusion(df_all_ind, date, df_forecast)

df_conclusion = generate_conclusion(df_all_ind, date, df_forecast)
# Appliquer les styles
df_conclusion_styled = apply_styles(df_conclusion)

# Afficher le résultat
df_conclusion_styled


#_______________________________________________________________________________________________________________________
