import requests #68S617QRYKZHX4ZN #I1TVUXGTKDYPXB78
import pandas as pd
import streamlit as st 
import plotly 
import numpy as np
import plotly.graph_objects as go
import altair as alt
import plotly.express as px
from datetime import datetime
import base64
#_______________________________________________________________________________________________________________________

def drop_unnamed_columns(df):
    return df.loc[:, ~df.columns.str.contains('^Unnamed')]

#_______________________________________________________________________________________________________________________


def process_dataframe(df, commodity_name):
    df['value'].replace('.', pd.NA, inplace=True)
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna(subset=['value'])
    df.drop(columns=[commodity_name], inplace=True)
    df.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')
    df.rename(columns={'value': f'value_{commodity_name}'}, inplace=True)
    df.set_index('date', inplace=True)
    return df

#_______________________________________________________________________________________________________________________


def drop_columns(df, *columns):
    return df.drop(columns=list(columns), inplace=False)

#_______________________________________________________________________________________________________________________

def compute_rsi(data, window=14):
    # Inverser les données avant de calculer le RSI
    reversed_data = data.iloc[::-1]
    
    # Calcul des variations
    delta = reversed_data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    # Calcul du Relative Strength (RS) et RSI
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Réinverser les résultats pour revenir à l'ordre chronologique original
    return rsi.iloc[::-1]

#_______________________________________________________________________________________________________________________
def compute_stochastics(data, window=14):

    reversed_data = data.iloc[::-1]
    
    # Calculer le stochastique sur les données inversées
    min_val = reversed_data.rolling(window=window).min()
    max_val = reversed_data.rolling(window=window).max()
    stoch = 100 * (reversed_data - min_val) / (max_val - min_val)
    
    # Réinverser les résultats pour revenir à l'ordre chronologique original
    return stoch.iloc[::-1]

#_______________________________________________________________________________________________________________________


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



#_______________________________________________________________________________________________________________________


def generer_nom_fichier(commodite, periode):
    return f"{commodite.lower()}_{periode}.py"

#_______________________________________________________________________________________________________________________

def generer_nom_fichier_fc(commodite):
    return f"{commodite.lower()}_fc.py"

#_______________________________________________________________________________________________________________________


def moyenne_mobile_simple(data, window_size, n_periods):
    data = data[::-1]
    
    # Initialisation de la série lissée
    sma = [np.nan] * (window_size - 1)  # Valeurs NaN pour les premières périodes (avant la fenêtre)
    
    # Appliquer la moyenne mobile simple
    for t in range(window_size - 1, len(data)):
        sma.append(np.mean(data[t - window_size + 1:t + 1]))
    
    # Calcul de la pente (approximation linéaire)
    if len(data) >= 2:
        slope = (data[-1] - data[-2]) / 1  # Différence entre les deux derniers points
    else:
        slope = 0
    
    # Prévisions : inclure une tendance dans les prévisions
    forecasts = []
    last_sma = sma[-1]
    for t in range(1, n_periods + 1):
        forecasts.append(last_sma + t * slope)  # Inclure la tendance linéaire
    
    # Inverser les résultats pour les ramener dans l'ordre d'origine (du plus récent au plus ancien)
    #sma = sma[::-1]
    #forecasts = forecasts[::-1]
    
    return forecasts


#_______________________________________________________________________________________________________________________
def lissage_exponentiel_simple(data, alpha, n_periods):
    # Initialisation de la série lissée avec la première valeur
    data = data[::-1]
    S = [data[0]]
    
    # Appliquer le lissage exponentiel simple
    for t in range(1, len(data)):
        S_new = alpha * data[t] + (1 - alpha) * S[t-1]
        S.append(S_new)
    
    # Calculer une tendance simple (différence entre les dernières valeurs lissées)
    if len(S) > 1:
        trend = S[-1] - S[-2]  # Tendance basée sur les deux dernières valeurs lissées
    else:
        trend = 0  # Pas de tendance si une seule valeur
    
    # Prévisions : ajouter la tendance à la dernière valeur lissée
    forecasts = [S[-1] + i * trend for i in range(1, n_periods + 1)]
    forecasts = forecasts[::-1]
    return S, forecasts

#_______________________________________________________________________________________________________________________
def lissage_exponentiel_double(data, alpha, beta, n_periods):

    n = len(data)
    data = data[::-1]

    # Initialisation
    L = [data[0]]  # Niveau initial
    T = [(data[1] - data[0]) if len(data) > 1 else 0]  # Tendance initiale
    LED = [L[0] + T[0]]  # Série LED

    # Appliquer LED
    for t in range(1, n):
        L_new = alpha * data[t] + (1 - alpha) * (L[t-1] + T[t-1])
        T_new = beta * (L_new - L[t-1]) + (1 - beta) * T[t-1]
        L.append(L_new)
        T.append(T_new)
        LED.append(L_new + T_new)
    
    # Prévisions pour les périodes futures
    forecasts = [L[-1] + (i + 1) * T[-1] for i in range(n_periods)]
    
    return LED, forecasts


#_______________________________________________________________________________________________________________________
def holt_winters(data, alpha, beta, gamma, season_length, n_periods):
    
    data = data[::-1]
    if len(data) < season_length:
        raise ValueError("Les données doivent contenir au moins autant d'observations que la saisonnalité.")
    
    # Initialisation des composantes
    L = [np.mean(data[:season_length])]  # Niveau initial
    T = [(np.mean(data[season_length:2 * season_length]) - np.mean(data[:season_length])) / season_length]  # Tendance initiale
    S = [data[i] / L[0] for i in range(season_length)]  # Saison initiale

    # Extension pour la saisonnalité
    S = S * ((len(data) // season_length) + 1)

    # Calcul des composantes
    for t in range(season_length, len(data)):
        L_new = alpha * (data[t] / S[t - season_length]) + (1 - alpha) * (L[-1] + T[-1])
        T_new = beta * (L_new - L[-1]) + (1 - beta) * T[-1]
        S_new = gamma * (data[t] / L_new) + (1 - gamma) * S[t - season_length]

        L.append(L_new)
        T.append(T_new)
        S[t] = S_new  # Mise à jour de la saisonnalité pour l'instant t

    # Prévisions Holt-Winters
    forecasts = []
    for i in range(1, n_periods + 1):
        forecasts.append((L[-1] + i * T[-1]) * S[-season_length + (i % season_length)])

    return L, forecasts

#_______________________________________________________________________________________________________________________

def add_anchor(name):
    st.markdown(f'<a id="{name}"></a>', unsafe_allow_html=True)

#_______________________________________________________________________________________________________________________

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
#_______________________________________________________________________________________________________________________

# Convertir directement image en HTML
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
#_______________________________________________________________________________________________________________________


#_______________________________________________________________________________________________________________________
