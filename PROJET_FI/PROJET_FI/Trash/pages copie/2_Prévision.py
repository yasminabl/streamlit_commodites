
import requests #68S617QRYKZHX4ZN #I1TVUXGTKDYPXB78
import pandas as pd
import streamlit as st 
import plotly 
import numpy as np
import plotly.graph_objects as go
import altair as alt
import plotly.express as px
from datetime import datetime, timedelta
from functions import *
import os 


df_wheat = pd.read_csv("df_wheat.csv", index_col=None)
df_corn = pd.read_csv("df_corn.csv", index_col=None)
df_coffee = pd.read_csv("df_coffee.csv", index_col=None)
df_index = pd.read_csv("df_index.csv", index_col=None)
df_sugar = pd.read_csv("df_sugar.csv", index_col=None)


#_______________________________________________________________________________________________________________________



# Options de sélection dans la sidebar
st.sidebar.subheader("Commodité à prévoir")
commodite = st.sidebar.radio("Sélectionnez une commodité :", ("all","coffee", "sugar", "corn", "wheat", "index"))

# Définir les chemins de dossiers pour les scripts
dossier = "pages/previsions/"  # Chemin vers le répertoire "previsions"
nom_fichier_fc = generer_nom_fichier_fc(commodite)  # Exemple: "coffee_fc.py"
chemin_fichier = os.path.join(dossier, nom_fichier_fc)  # "pages/previsions/coffee_fc.py"

if os.path.exists(chemin_fichier):
    with open(chemin_fichier) as f:
        try:
            exec(f.read())  # Exécute le code du fichier Python
        except Exception as e:
            st.error(f"Erreur lors de l'exécution du fichier {nom_fichier_fc}: {str(e)}")





#_______________________________________________________________________________________________________________________
