
import requests #68S617QRYKZHX4ZN #I1TVUXGTKDYPXB78
import pandas as pd
import streamlit as st 
import plotly 
import numpy as np
import plotly.graph_objects as go
import altair as alt
import plotly.express as px
from datetime import datetime, timedelta
from features.functions import *
import os 


df_wheat = pd.read_csv("df_wheat.csv", index_col=None)
df_corn = pd.read_csv("df_corn.csv", index_col=None)
df_coffee = pd.read_csv("df_coffee.csv", index_col=None)
df_index = pd.read_csv("df_index.csv", index_col=None)
df_sugar = pd.read_csv("df_sugar.csv", index_col=None)


#_______________________________________________________________________________________________________________________



# Options de sélection dans la sidebar
st.sidebar.subheader("Période d'analyse")
periode = st.sidebar.radio("Sélectionnez la période :", ("Long terme (toutes les données)","Court terme (1 an)"))
commodite = st.sidebar.radio("Sélectionnez une commodité :", ("all","coffee", "sugar", "corn", "wheat", "index"))

# Définir les chemins de dossiers pour les scripts
dossier_court_terme = "pages/court_terme/"
dossier_long_terme = "pages/long_terme/"
nom_fichier = None

# Définir le dossier en fonction de la période
dossier = dossier_court_terme  # Dossier par défaut
if periode == "Court terme (1 an)":
    # Si période court terme, générer le nom de fichier avec suffixe "st"
    nom_fichier_st = generer_nom_fichier(commodite, "st")  # Exemple: "coffee_st.py"
    chemin_fichier = os.path.join(dossier, nom_fichier_st)
else:
    # Si période long terme, générer le nom de fichier avec suffixe "lt"
    dossier = dossier_long_terme  # Changer de dossier pour long terme
    nom_fichier_lt = generer_nom_fichier(commodite, "lt")  # Exemple: "coffee_lt.py"
    chemin_fichier = os.path.join(dossier, nom_fichier_lt)


# Charger et exécuter le script Python correspondant
try:
    with open(chemin_fichier) as file:
        exec(file.read())
except FileNotFoundError:
    st.error(f"Le fichier {nom_fichier} pour {commodite} dans {periode} n'existe pas.")
except Exception as e:
    st.error(f"Une erreur s'est produite lors de l'exécution du fichier {nom_fichier} : {e}")

#_______________________________________________________________________________________________________________________
