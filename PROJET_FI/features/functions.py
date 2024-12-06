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
import os 


'''
1_Supprime_colonne_unnamed
2_Nettoie_Données
3_Supprime_colonne
4_Calcul_RSI
5_Calcul_Stochastic
6_Creer_DataFrame_From_API
7_Genere_nom_fichier
8_Genere_nom_image
9_Prevision_moyenne_mobile
10_Prevision_les
11_Prevision_led
12_Prevision_holt_&_winter
13_Encrage_lien_inter
14_Convertir_image_HTML
15_Nettoie_Dataframe
16_Inverse_Dataframe
17_Ajoute_Indicateurs
18_Filtre_Dataframe
19_Sidebar_select_date
20_Sidebar_choix_commodite
21_Graphique_cours_boursier
22_Graphique_indicateurs
23_Graphique_indicateurs_all
24_Genere_nom_fichier_prevision
25_Dataframe_Conclusion
26_Graphique_Prevision_Moyenne_Mobile
27_Graphique_Prevision_LES
28_Graphique_Prevision_LED
29_Graphique_Prevision_Holt_&_Winter
30_Tableau_Holt_&_Winter
31_Tableau_Conclusion
32_tableau descriptif


'''
#___________________________________________________________________________________________________________________________________________

#                                                   1_Supprime_colonne_unnamed
#___________________________________________________________________________________________________________________________________________

def drop_unnamed_columns(df):
    return df.loc[:, ~df.columns.str.contains('^Unnamed')]

#___________________________________________________________________________________________________________________________________________

#                                                   2_Nettoie_Données
#___________________________________________________________________________________________________________________________________________


def process_dataframe(df, commodity_name):
    df['value'].replace('.', pd.NA, inplace=True)
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna(subset=['value'])
    df.drop(columns=[commodity_name], inplace=True)
    df.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')
    df.rename(columns={'value': f'value_{commodity_name}'}, inplace=True)
    df.set_index('date', inplace=True)
    return df

#___________________________________________________________________________________________________________________________________________

#                                                   3_Supprime_colonne
#___________________________________________________________________________________________________________________________________________


def drop_columns(df, *columns):
    return df.drop(columns=list(columns), inplace=False)

#___________________________________________________________________________________________________________________________________________

#                                                   4_Calcul_RSI
#___________________________________________________________________________________________________________________________________________

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

#___________________________________________________________________________________________________________________________________________

#                                                   5_Calcul_Stochastic
#___________________________________________________________________________________________________________________________________________

def compute_stochastics(data, window=14):

    reversed_data = data.iloc[::-1]
    
    # Calculer le stochastique sur les données inversées
    min_val = reversed_data.rolling(window=window).min()
    max_val = reversed_data.rolling(window=window).max()
    stoch = 100 * (reversed_data - min_val) / (max_val - min_val)
    
    # Réinverser les résultats pour revenir à l'ordre chronologique original
    return stoch.iloc[::-1]

#___________________________________________________________________________________________________________________________________________

#                                                   6_Creer_DataFrame_From_API
#___________________________________________________________________________________________________________________________________________

'''
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
'''


#___________________________________________________________________________________________________________________________________________

#                                                   7_Genere_nom_fichier
#___________________________________________________________________________________________________________________________________________


def generer_nom_fichier(commodite, periode):
    return f"{commodite.lower()}_{periode}.py"

#___________________________________________________________________________________________________________________________________________

#                                                   8_Genere_nom_image
#___________________________________________________________________________________________________________________________________________

def generer_nom_image(commodite):
    return f"{commodite}.png"

#___________________________________________________________________________________________________________________________________________

#                                                   9_Prevision_moyenne_mobile
#___________________________________________________________________________________________________________________________________________

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

#____________________________________________________________________________________________________________________________________________

#                                                   10_Prevision_les
#____________________________________________________________________________________________________________________________________________

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

#____________________________________________________________________________________________________________________________________________

#                                                   11_Prevision_led
#____________________________________________________________________________________________________________________________________________

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

#____________________________________________________________________________________________________________________________________________

#                                                   12_Prevision_holt_&_winter
#____________________________________________________________________________________________________________________________________________


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

#____________________________________________________________________________________________________________________________________________

#                                                   13_Encrage_lien_inter
#____________________________________________________________________________________________________________________________________________

def add_anchor(name):
    st.markdown(f'<a id="{name}"></a>', unsafe_allow_html=True)

#____________________________________________________________________________________________________________________________________________

#                                                   14_Convertir_image_HTML
#____________________________________________________________________________________________________________________________________________

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
    
#____________________________________________________________________________________________________________________________________________

#                                                   15_Nettoie_Dataframe
#____________________________________________________________________________________________________________________________________________

def clean_df(df, commodite):
    df = process_dataframe(df, commodite)
    df = drop_unnamed_columns(df)
    return df

#____________________________________________________________________________________________________________________________________________

#                                                   16_Inverse_Dataframe
#____________________________________________________________________________________________________________________________________________

def reverse_dataframe(df):
    return df.iloc[::-1].reset_index(drop=True)

#____________________________________________________________________________________________________________________________________________

#                                                   17_Ajout_Indicateurs
#____________________________________________________________________________________________________________________________________________

def df_ind(df, commodite):
    df[f'MM_20_{commodite}'] = df[f'value_{commodite}'].iloc[::-1].rolling(window=20).mean().iloc[::-1]
    df[f'MM_200_{commodite}'] =df[f'value_{commodite}'].iloc[::-1].rolling(window=200).mean().iloc[::-1]
    df[f'RSI_{commodite}'] = compute_rsi(df[f'value_{commodite}'])
    df[f'Stochastic_{commodite}'] = compute_stochastics(df[f'value_{commodite}'])
    return df

#____________________________________________________________________________________________________________________________________________

#                                                   18_Filtre_Dataframe
#____________________________________________________________________________________________________________________________________________

def filter_dataframe(df, selected_year_min, selected_month_min, selected_year_max, selected_month_max):
    # Construction des dates de début et de fin
    start_date = pd.Timestamp(year=selected_year_min, month=selected_month_min, day=1)
    end_date = pd.Timestamp(year=selected_year_max, month=selected_month_max, day=1) + pd.offsets.MonthEnd(1)

    # Filtrage des DataFrames
    df_filtered = df[(df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))]
    return df_filtered

#_______________________________________________________________________________________________________________________

#                                                   19_Sidebar_select_date
#____________________________________________________________________________________________________________________________________________

def get_date_range_from_sidebar(df, sidebar_title="Filtrer les données par date"):
    # Convertir l'index en DatetimeIndex si ce n'est pas déjà le cas
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    # Récupération des années et des mois uniques
    years = df.index.year.unique()
    months = range(1, 13)

    # Mois actuels (par défaut)
    last_month = df.index[-1].month
    current_month = df.index[0].month

    # Widgets Streamlit pour sélectionner la plage de dates
    st.sidebar.title(sidebar_title)
    selected_year_min = st.sidebar.selectbox("Sélectionnez l'année de départ", options=years, index=len(years) - 1)
    selected_month_min = st.sidebar.selectbox("Sélectionnez le mois de départ", options=months, index=list(months).index(last_month))

    selected_year_max = st.sidebar.selectbox("Sélectionnez l'année de fin", options=years, index=0)
    selected_month_max = st.sidebar.selectbox("Sélectionnez le mois de fin", options=months, index=list(months).index(current_month))

    return selected_year_min, selected_month_min, selected_year_max, selected_month_max


#__________________________________________________20_Sidebar_choix_commodite________________________________________________

def select_commodities(commodite, unique_id):
    selected_commodities = st.sidebar.radio(
        "Sélectionnez la commodité",  
        [commodite, "Index", "Les deux"],
        index=2,
        key=f"radio_{commodite}_{unique_id}")
    return selected_commodities

#____________________________________________________________________________________________________________________________________________

#                                                   20_Graphique_cours_boursier
#____________________________________________________________________________________________________________________________________________


import plotly.graph_objects as go
import streamlit as st

def graph_cours_boursier(df, selected_commodity, commodite):
    """
    Affiche un graphique des cours boursiers avec un titre stylisé en bas.
    """
    # Définir les colonnes à afficher et le titre en fonction de la commodité sélectionnée
    if selected_commodity == commodite:
        columns_to_display = [f'value_{commodite}']
        title_to_display = f'Graphique du {commodite}'
    elif selected_commodity == "Index":
        columns_to_display = ['value_index']
        title_to_display = 'Graphique de l\'index'
    else:  # "Les deux"
        columns_to_display = [f'value_{commodite}', 'value_index']
        title_to_display = f'Graphique du {commodite} et de l\'index'

    # Créer le graphique avec Plotly
    fig = go.Figure()

    # Ajouter une trace pour chaque colonne sélectionnée
    for column in columns_to_display:
        fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column))

    # Mise en forme du graphique
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Valeurs boursières ($)",
        legend_title="Cours boursier",
        template="plotly_dark",
    )

    # Retourner le graphique et le titre stylisé
    return fig, title_to_display

def display_graphs(fig1, title1, fig2, title2, text_column_content):
    """
    Affiche deux graphiques et une colonne de texte explicatif dans une disposition à trois colonnes.
    Ajoute un titre stylisé sous chaque graphique.
    :param fig1: Premier graphique à afficher (Plotly Figure).
    :param title1: Titre du premier graphique.
    :param fig2: Deuxième graphique à afficher (Plotly Figure).
    :param title2: Titre du deuxième graphique.
    :param text_column_content: Contenu HTML pour la colonne de texte explicatif.
    """
    # CSS pour le style
    st.markdown(
        """
        <style>
        /* Style global pour les colonnes */
        .custom-column {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
        }

        /* Style des titres des graphiques */
        .graph-title {
            font-size: 18px;
            font-weight: bold;
            text-decoration: underline;
            font-family: 'Poppins', sans-serif;
            color: #ffffff;
            margin-top: 10px;
            text-align: center;
        }

        /* Style de la carte des faits */
        .facts-card {
            border: 2px solid white;
            border-radius: 15px;
            padding: 15px;
            background-color: #000000;
            color: white;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.5);
        }

        /* Titre de la carte */
        .facts-title {
            color: white;
            text-align: center;
            font-family: 'Playfair Display', serif;
            font-size: 20px;
            margin-bottom: 10px;
        }

        /* Contenu de la carte */
        .facts-content {
            text-align: justify;
            font-family: 'Poppins', sans-serif;
            font-size: 14px;
            line-height: 1.6;
            color: #bbbbbb;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Configuration des colonnes
    col1, col2, col3 = st.columns(3)

    # Graphique 1
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown(
            f"""
            <div class="graph-title">{title1}</div>
            """,
            unsafe_allow_html=True,
        )

    # Graphique 2
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(
            f"""
            <div class="graph-title">{title2}</div>
            """,
            unsafe_allow_html=True,
        )

    # Carte des faits en bref
    with col3:
        st.markdown(
            f"""
            <div class="facts-card">
                <h3 class="facts-title">Faits en bref</h3>
                <div class="facts-content">{text_column_content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


#_______________________


def graph_cours_boursier_long_term(df, selected_commodity, commodite):
    """
    Affiche un graphique des cours boursiers à long terme avec un titre stylisé en bas.
    """
    # Définir les colonnes à afficher et le titre en fonction de la commodité sélectionnée
    if selected_commodity == commodite:
        columns_to_display = [f'value_{commodite}']
        title_to_display = f'Graphique à long terme du {commodite}'
    elif selected_commodity == "Index":
        columns_to_display = ['value_index']
        title_to_display = 'Graphique à long terme de l\'index'
    else:  # "Les deux"
        columns_to_display = [f'value_{commodite}', 'value_index']
        title_to_display = f'Graphique à long terme du {commodite} et de l\'index'

    # Créer le graphique avec Plotly
    fig = go.Figure()

    # Ajouter une trace pour chaque colonne sélectionnée
    for column in columns_to_display:
        fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column))

    # Mise en forme du graphique
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Valeurs boursières ($)",
        legend_title="Cours boursier",
        template="plotly_dark",
    )

    # Retourner le graphique et le titre stylisé
    return fig, title_to_display

def display_graphs_long_term(fig1, title1, fig2, title2, text_column_content):
    """
    Affiche deux graphiques à long terme et une colonne de texte explicatif dans une disposition à trois colonnes.
    Ajoute un titre stylisé en bas à gauche sous chaque graphique.
    :param fig1: Premier graphique à afficher (Plotly Figure).
    :param title1: Titre du premier graphique.
    :param fig2: Deuxième graphique à afficher (Plotly Figure).
    :param title2: Titre du deuxième graphique.
    :param text_column_content: Contenu HTML pour la colonne de texte explicatif.
    """
    # CSS pour le style
    st.markdown(
        """
        <style>
        /* Style global pour les colonnes */
        .custom-column {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
        }

        /* Style des titres des graphiques */
        .graph-title-bottom-left {
            font-size: 12px;
            font-weight: bold;
            text-decoration: underline;
            font-family: 'Poppins', sans-serif;
            color: #ffffff;
            margin-top: 10px;
            text-align: left;
            margin-left: 5px; /* Décalage à gauche */
        }

        /* Style de la carte des faits */
        .facts-card {
            border: 2px solid white;
            border-radius: 15px;
            padding: 15px;
            background-color: #000000;
            color: white;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.5);
        }

        /* Titre de la carte */
        .facts-title {
            color: white;
            text-align: center;
            font-family: 'Playfair Display', serif;
            font-size: 20px;
            margin-bottom: 10px;
        }

        /* Contenu de la carte */
        .facts-content {
            text-align: justify;
            font-family: 'Poppins', sans-serif;
            font-size: 14px;
            line-height: 1.6;
            color: #bbbbbb;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Configuration des colonnes
    col1, col2, col3 = st.columns(3)

    # Graphique 1
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown(
            f"""
            <div class="graph-title-bottom-left">{title1}</div>
            """,
            unsafe_allow_html=True,
        )

    # Graphique 2
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(
            f"""
            <div class="graph-title-bottom-left">{title2}</div>
            """,
            unsafe_allow_html=True,
        )

    # Carte des faits en bref
    with col3:
        st.markdown(
            f"""
            <div class="facts-card">
                <h3 class="facts-title">Faits en bref</h3>
                <div class="facts-content">{text_column_content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# _______________________________________
# Utilisation des fonctions pour le long terme
# _______________________________________

def graph_cours_boursier_long_term(df, selected_commodity, commodite):
    """
    Affiche un graphique des cours boursiers à long terme avec un titre stylisé en bas.
    """
    # Définir les colonnes à afficher et le titre en fonction de la commodité sélectionnée
    if selected_commodity == commodite:
        columns_to_display = [f'value_{commodite}']
        title_to_display = f'Graphique à long terme du {commodite}'
    elif selected_commodity == "Index":
        columns_to_display = ['value_index']
        title_to_display = 'Graphique à long terme de l\'index'
    else:  # "Les deux"
        columns_to_display = [f'value_{commodite}', 'value_index']
        title_to_display = f'Graphique à long terme du {commodite} et de l\'index'

    # Créer le graphique avec Plotly
    fig = go.Figure()

    # Ajouter une trace pour chaque colonne sélectionnée
    for column in columns_to_display:
        fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column))

    # Mise en forme du graphique
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Valeurs boursières ($)",
        legend_title="Cours boursier",
        template="plotly_dark",
    )

    # Retourner le graphique et le titre stylisé
    return fig, title_to_display

def display_graphs_long_term(fig1, title1, fig2, title2, text_column_content):
    """
    Affiche deux graphiques à long terme et une colonne de texte explicatif dans une disposition à trois colonnes.
    Ajoute un titre stylisé sous chaque graphique.
    :param fig1: Premier graphique à afficher (Plotly Figure).
    :param title1: Titre du premier graphique.
    :param fig2: Deuxième graphique à afficher (Plotly Figure).
    :param title2: Titre du deuxième graphique.
    :param text_column_content: Contenu HTML pour la colonne de texte explicatif.
    """
    # CSS pour le style
    st.markdown(
        """
        <style>
        /* Style global pour les colonnes */
        .custom-column {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
        }

        /* Style des titres des graphiques */
        .graph-title {
            font-size: 18px;
            font-weight: bold;
            text-decoration: underline;
            font-family: 'Poppins', sans-serif;
            color: #ffffff;
            margin-top: 10px;
            text-align: center;
        }

        /* Style de la carte des faits */
        .facts-card {
            border: 2px solid white;
            border-radius: 15px;
            padding: 15px;
            background-color: #000000;
            color: white;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.5);
        }

        /* Titre de la carte */
        .facts-title {
            color: white;
            text-align: center;
            font-family: 'Playfair Display', serif;
            font-size: 20px;
            margin-bottom: 10px;
        }

        /* Contenu de la carte */
        .facts-content {
            text-align: justify;
            font-family: 'Poppins', sans-serif;
            font-size: 14px;
            line-height: 1.6;
            color: #bbbbbb;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Configuration des colonnes
    col1, col2, col3 = st.columns(3)

    # Graphique 1
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown(
            f"""
            <div class="graph-title">{title1}</div>
            """,
            unsafe_allow_html=True,
        )

    # Graphique 2
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(
            f"""
            <div class="graph-title">{title2}</div>
            """,
            unsafe_allow_html=True,
        )

    # Carte des faits en bref
    with col3:
        st.markdown(
            f"""
            <div class="facts-card">
                <h3 class="facts-title">Perspectives à long terme</h3>
                <div class="facts-content">{text_column_content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )




#____________________________________________________________________________________________________________________________________________

#                                                   21_Graphique_indicateurs
#____________________________________________________________________________________________________________________________________________

def graph_indicateurs(df, commodite, selected_indicators):
    fig = go.Figure()

    # Ajout des traces
    if f'MM_{commodite}' in selected_indicators:
        fig.add_trace(go.Scatter(x=df.index, y=df[f'MM_20_{commodite}'], mode='lines', name='MM 20'))
        fig.add_trace(go.Scatter(x=df.index, y=df[f'value_{commodite}'], mode='lines', name=f'Cours de {commodite}'))
        fig.add_trace(go.Scatter(x=df.index, y=df[f'MM_200_{commodite}'], mode='lines', name='MM 200'))

    if f'RSI_{commodite}' in selected_indicators:
        fig.add_trace(go.Scatter(x=df.index, y=df[f'RSI_{commodite}'], mode='lines', name='RSI'))

    if f'Stochastic_{commodite}' in selected_indicators:
        fig.add_trace(go.Scatter(x=df.index, y=df[f'Stochastic_{commodite}'], mode='lines', name='Stochastic'))

    # Mise en forme du graphique
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Valeurs boursières ($)",
        legend_title="Indicateurs"
    )

    return fig

#____________________________________________________________________________________________________________________________________________

#                                                   22_Graphique_indicateurs_all
#____________________________________________________________________________________________________________________________________________

def graph_all(df, selected_items):

    fig = go.Figure()

    for item in selected_items:
        # Ajouter le préfixe 'value_' aux éléments sélectionnés
        column_name = f"value_{item}"  # Ajouter le préfixe 'value_' à l'item

        # Vérifier si la colonne avec le préfixe existe dans le DataFrame
        if column_name in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index, 
                    y=df[column_name],  # Utilisation correcte de la colonne avec le préfixe 'value_'
                    mode="lines", 
                    name=item
                )
            )
    fig.update_layout(
    title="Graphique des Commodités",
    xaxis_title="Date",
    yaxis_title="Valeur",
    legend_title="Commodités"
)
    st.plotly_chart(fig)

#____________________________________________________________________________________________________________________________________________

#                                                   23_Genere_nom_fichier_prevision
#____________________________________________________________________________________________________________________________________________


def generer_nom_fichier_fc(commodite):
    return f"{commodite.lower()}_fc.py"

#____________________________________________________________________________________________________________________________________________

#                                                   24_Graphique_Prevision_Moyenne_Mobile
#____________________________________________________________________________________________________________________________________________

def generate_mm_forecasts_and_plot(df_dict, forecast_horizon, selected_commodities_mm):

    # Initialisation des variables communes
    current_month_start = pd.to_datetime('today').replace(day=1)  # Début du mois actuel
    fig_mm = go.Figure()

    for commodity, df in df_dict.items():
        # Étape 1 : Ajuster l'index pour chaque commodité
        df.index = pd.date_range(start=current_month_start, periods=len(df), freq='-1MS')

        # Étape 2 : Calcul des prévisions avec un index d'extension
        last_date = df.index[0]
        forecast_index = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_horizon, freq='MS')

        # Utilisation de votre fonction moyenne_mobile_simple
        df_mm = pd.DataFrame(
            moyenne_mobile_simple(df[f'value_{commodity}'], 4, forecast_horizon),
            index=forecast_index,
            columns=[f'MM_{commodity}']
        )

        # Étape 3 : Concaténation des données historiques et des prévisions
        df_historical = df.copy()
        df_historical[f'MM_{commodity}'] = np.nan

        df_forecast = pd.DataFrame(index=forecast_index)
        df_forecast[f'value_{commodity}'] = np.nan
        df_forecast[f'MM_{commodity}'] = df_mm[f'MM_{commodity}']
        df_forecast = df_forecast[::-1]

        df_final = pd.concat([df_forecast, df_historical])

        # Ajout des traces au graphique si la commodité est sélectionnée
        if f'MM_{commodity}' in selected_commodities_mm:
            fig_mm.add_trace(go.Scatter(
                x=df_final.index,
                y=df_final[f'value_{commodity}'],
                mode='lines',
                name=f'value_{commodity}'
            ))
            fig_mm.add_trace(go.Scatter(
                x=df_final.index,
                y=df_final[f'MM_{commodity}'],
                mode='lines',
                name=f'MM_{commodity}'
            ))

    # Mise à jour du layout du graphique
    fig_mm.update_layout(
        title="Graphique prévisionnel des cours boursiers selon la moyenne mobile",
        xaxis_title="Date",
        yaxis_title="Valeur du cours ($)",
        legend_title="Commodités"
    )

    return fig_mm

#____________________________________________________________________________________________________________________________________________

#                                                   25_Graphique_Prevision_LES
#____________________________________________________________________________________________________________________________________________

def generate_les_forecasts_and_plot(df_dict_les, forecast_horizon, alpha, selected_commodities_les):

    # Initialisation
    current_month_start = pd.to_datetime('today').replace(day=1)  # Début du mois actuel
    fig_les = go.Figure()

    for commodity, df in df_dict_les.items():
        # Étape 1 : Ajuster l'index pour chaque commodité
        df.index = pd.date_range(start=current_month_start, periods=len(df), freq='-1MS')

        # Étape 2 : Calcul des prévisions avec un index d'extension
        last_date = df.index[0]
        forecast_index = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_horizon, freq='MS')

        # Application du lissage exponentiel simple
        _, forecasts = lissage_exponentiel_simple(df[f'value_{commodity}'].values, alpha, forecast_horizon)

        # Étape 3 : Construire les deux parties du DataFrame final
        # Partie historique : uniquement les données brutes historiques
        df_historical = df.copy()

        # Partie prévisions : uniquement les prévisions LES
        df_forecast = pd.DataFrame(index=forecast_index[::-1])  # Index inversé
        df_forecast[f'value_{commodity}'] = np.nan  # Aucune donnée brute pour les prévisions
        df_forecast[f'LES_{commodity}'] = forecasts  # Ajouter les prévisions LES

        # Concaténation
        df_final = pd.concat([df_forecast, df_historical])

        # Ajout des traces au graphique si la commodité est sélectionnée
        if f'LES_{commodity}' in selected_commodities_les:
            fig_les.add_trace(go.Scatter(
                x=df_final.index,
                y=df_final[f'value_{commodity}'],
                mode='lines',
                name=f'value_{commodity}'
            ))
            fig_les.add_trace(go.Scatter(
                x=df_final.index,
                y=df_final[f'LES_{commodity}'],
                mode='lines',
                name=f'LES_{commodity}'
            ))

    # Mise à jour du layout du graphique
    fig_les.update_layout(
        title="Graphique prévisionnel des cours boursiers selon le LES",
        xaxis_title="Date",
        yaxis_title="Valeur du cours ($)",
        legend_title="Commodités"
    )

    return fig_les


#____________________________________________________________________________________________________________________________________________

#                                                   26_Graphique_Prevision_LED
#____________________________________________________________________________________________________________________________________________

def generate_led_forecasts_and_plot(df_dict_led, forecast_horizon, alpha, beta, selected_commodities_led):

    # Initialisation
    current_month_start = pd.to_datetime('today').replace(day=1)  # Début du mois actuel
    fig_led = go.Figure()

    for commodity, df in df_dict_led.items():
        # Étape 1 : Ajuster l'index pour chaque commodité
        df.index = pd.date_range(start=current_month_start, periods=len(df), freq='-1MS')

        # Étape 2 : Calcul des prévisions avec un index d'extension
        last_date = df.index[0]
        forecast_index = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_horizon, freq='MS')

        # Application du lissage exponentiel simple
        _, forecasts = lissage_exponentiel_double(df[f'value_{commodity}'].values, alpha, beta, forecast_horizon)

        # Étape 3 : Construire les deux parties du DataFrame final
        # Partie historique : uniquement les données brutes historiques
        df_historical = df.copy()

        # Partie prévisions : uniquement les prévisions LES
        df_forecast = pd.DataFrame(index=forecast_index[::-1])  # Index inversé
        df_forecast[f'value_{commodity}'] = np.nan  # Aucune donnée brute pour les prévisions
        df_forecast[f'LED_{commodity}'] = forecasts[::-1]  # Ajouter les prévisions LES

        # Concaténation
        df_final = pd.concat([df_forecast, df_historical])

        # Ajout des traces au graphique si la commodité est sélectionnée
        if f'LED_{commodity}' in selected_commodities_led:
            fig_led.add_trace(go.Scatter(
                x=df_final.index,
                y=df_final[f'value_{commodity}'],
                mode='lines',
                name=f'value_{commodity}'
            ))
            fig_led.add_trace(go.Scatter(
                x=df_final.index,
                y=df_final[f'LED_{commodity}'],
                mode='lines',
                name=f'LED_{commodity}'
            ))

    # Mise à jour du layout du graphique
    fig_led.update_layout(
        title="Graphique prévisionnel des cours boursiers selon le LED",
        xaxis_title="Date",
        yaxis_title="Valeur du cours ($)",
        legend_title="Commodités"
    )

    return fig_led


#____________________________________________________________________________________________________________________________________________

#                                                   27_Graphique_Prevision_Holt_&_Winter
#____________________________________________________________________________________________________________________________________________


def generate_hw_forecasts_and_plot(df_dict_hw, forecast_horizon, alpha, beta, gamma, season_length, selected_commodities_hw):
    # Initialisation
    current_month_start = pd.to_datetime('today').replace(day=1)  # Début du mois actuel
    fig_hw = go.Figure()

    for commodity, df in df_dict_hw.items():
        # Étape 1 : Ajuster l'index pour chaque commodité
        df.index = pd.date_range(start=current_month_start, periods=len(df), freq='-1MS')

        # Étape 2 : Calcul des prévisions avec un index d'extension
        last_date = df.index[0]
        forecast_index = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_horizon, freq='MS')

        # Application du modèle Holt-Winters
        _, forecasts = holt_winters(df[f'value_{commodity}'].values, alpha, beta, gamma, season_length, forecast_horizon)

        # Étape 3 : Construire les deux parties du DataFrame final
        # Partie historique : uniquement les données brutes historiques
        df_historical = df.copy()

        # Partie prévisions : uniquement les prévisions HW
        df_forecast = pd.DataFrame(index=forecast_index[::-1])  # Index inversé
        df_forecast[f'value_{commodity}'] = np.nan  # Aucune donnée brute pour les prévisions
        df_forecast[f'H&W_{commodity}'] = forecasts[::-1]  # Ajouter les prévisions Holt-Winters

        # Concaténation
        df_final = pd.concat([df_forecast, df_historical])

        # Ajout des traces au graphique si la commodité est sélectionnée
        if f'H&W_{commodity}' in selected_commodities_hw:
            fig_hw.add_trace(go.Scatter(
                x=df_final.index,
                y=df_final[f'value_{commodity}'],
                mode='lines',
                name=f'value_{commodity}'
            ))
            fig_hw.add_trace(go.Scatter(
                x=df_final.index,
                y=df_final[f'H&W_{commodity}'],
                mode='lines',
                name=f'H&W_{commodity}'
            ))

    # Mise à jour du layout du graphique
    fig_hw.update_layout(
        title="Graphique prévisionnel des cours boursiers selon le H&W",
        xaxis_title="Date",
        yaxis_title="Valeur du cours ($)",
        legend_title="Commodités"
    )

    return fig_hw

#____________________________________________________________________________________________________________________________________________

#                                                   28_HW_Prevision
#____________________________________________________________________________________________________________________________________________

def generate_hw_forecasts(df_dict_hw, forecast_horizon, alpha, beta, gamma, season_length):
    # Initialisation
    current_month_start = pd.to_datetime('today').replace(day=1)  # Début du mois actuel
    forecast_df = pd.DataFrame()

    for commodity, df in df_dict_hw.items():
        # Ajuster l'index pour chaque commodité
        df.index = pd.date_range(start=current_month_start, periods=len(df), freq='-1MS')

        # Calcul des prévisions avec un index d'extension
        last_date = df.index[0]
        forecast_index = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_horizon, freq='MS')

        # Application du modèle Holt-Winters
        _, forecasts = holt_winters(df[f'value_{commodity}'].values, alpha, beta, gamma, season_length, forecast_horizon)

        # Création du DataFrame des prévisions
        df_forecast = pd.DataFrame(index=forecast_index[::-1])  # Index inversé pour ordre chronologique
        df_forecast[f'H&W_{commodity}'] = forecasts[::-1]  # Ajouter les prévisions Holt-Winters

        # Fusionner les prévisions dans le DataFrame principal
        forecast_df = pd.concat([forecast_df, df_forecast], axis=1)

    return forecast_df


#____________________________________________________________________________________________________________________________________________

#                                                   29_Tableau_Conclusion
#____________________________________________________________________________________________________________________________________________


def generate_conclusion(df_all_ind, date, forecast_df):
    df_conclusion = pd.DataFrame(
        columns=['coffee', 'sugar', 'corn', 'wheat', 'index'],
        index=['Tendance', 'Pression', 'Prévision']
    )
    
    # Liste des produits et colonnes associées
    commodites = ['coffee', 'sugar', 'corn', 'wheat', 'index']
    
    # Boucle sur chaque produit pour calculer les conclusions
    for commodite in commodites:
        mm_col = f"MM_20_{commodite}"  # Colonne de la moyenne mobile
        value_col = f"value_{commodite}"  # Colonne de la valeur
        rsi_col = f"RSI_{commodite}"  # Colonne de l'indicateur RSI
        forecast_col = f'H&W_{commodite}'  # Colonne de la prévision

        # Vérifier que les colonnes existent dans le DataFrame
        if all(col in df_all_ind.columns for col in [mm_col, value_col, rsi_col]):
            # Tendance
            if df_all_ind.loc[date, mm_col] > df_all_ind.loc[date, value_col]:
                df_conclusion.loc['Tendance', commodite] = 'Haussière'
            else:
                df_conclusion.loc['Tendance', commodite] = 'Baissière'
            
            # Pression
            rsi_value = df_all_ind.loc[date, rsi_col]
            if rsi_value > 80:
                df_conclusion.loc['Pression', commodite] = 'Vente'
            elif 20 < rsi_value <= 80:
                df_conclusion.loc['Pression', commodite] = 'Attente'
            else:
                df_conclusion.loc['Pression', commodite] = 'Achat'
            
            # Prévision
            # Comparer la première valeur de la prévision avec la première valeur dans df_all_ind
            if forecast_col in forecast_df.columns:
                forecast_value = forecast_df.loc[forecast_df.index[0], forecast_col]  # Première prévision
                current_value = df_all_ind.loc[date, value_col]  # Première valeur réelle
                if forecast_value > current_value:
                    df_conclusion.loc['Prévision', commodite] = 'Hausse'
                else:
                    df_conclusion.loc['Prévision', commodite] = 'Baisse'
        else:
            # Si des colonnes sont manquantes, on marque comme non disponible
            df_conclusion.loc['Tendance', commodite] = 'N/A'
            df_conclusion.loc['Pression', commodite] = 'N/A'
            df_conclusion.loc['Prévision', commodite] = 'N/A'
    
    return df_conclusion

#____________________________________________________________________________________________________________________________________________

#                                                   30_tableau descriptif
#____________________________________________________________________________________________________________________________________________


def display_custom_table(dataframe, legend_title):
    # Calcul des statistiques descriptives et transformation
    desc = dataframe.describe()
    desc_trans = desc.T.round(2)  # Transpose et arrondit à deux décimales

    # CSS pour personnaliser le tableau
    st.markdown(
        """
        <style>
        .custom-table-container {
            border: 4px solid #FFFFFF; /* Bordure blanche externe */
            border-radius: 15px; /* Coins arrondis */
            padding: 20px; /* Espace entre le tableau et la bordure */
            margin: 20px auto; /* Espacement vertical et centrage horizontal */
            background-color: #FFFFFF; /* Fond blanc entre la bordure et le tableau */
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.5); /* Effet d'ombre */
            width: 100%; /* Prend toute la largeur de la page */
        }
        .custom-table {
            width: 100%; /* Prend toute la largeur disponible */
            border-collapse: collapse; /* Fusionner les bordures */
            background-color: #000000; /* Fond noir du tableau */
        }
        .custom-table th, .custom-table td {
            border: 1px solid #FFFFFF; /* Bordures des cellules en blanc */
            padding: 10px;
            text-align: center; /* Alignement centré */
            color: #FFFFFF; /* Texte blanc */
        }
        .custom-table th {
            font-weight: bold; /* Titres en gras */
            background-color: #1E1E1E; /* Fond légèrement plus clair pour les titres */
            color: #FFFFFF; /* Texte blanc pour les titres */
        }
        .table-legend {
            text-align: left; /* Légende alignée à gauche */
            font-size: 16px;
            font-weight: bold;
            text-decoration: underline; /* Souligne la légende */
            color: #FFFFFF; /* Couleur blanche pour la légende */
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Convertir le DataFrame en HTML pour Streamlit
    table_html = desc_trans.to_html(classes="custom-table", border=0, escape=False)

    # Afficher le tableau dans une "carte" avec bordure blanche et intérieur noir
    st.markdown(f"<div class='custom-table-container'>{table_html}</div>", unsafe_allow_html=True)

    # Ajouter une légende sous le tableau, alignée à gauche
    st.markdown(f"<div class='table-legend'>{legend_title}</div>", unsafe_allow_html=True)



#____________________________________________________________________________________________________________________________________________

#                                                   Sauvegarde_API_CSV
#____________________________________________________________________________________________________________________________________________


#______________________________32_tableau descriptif_________________________________________________________________________________________

'''
df = create_df('coffee', 
          'https://www.alphavantage.co/query?function=COFFEE&interval=monthly',
          '68S617QRYKZHX4ZN')
df.to_csv('df_coffee.csv', index=False)  

df = create_df('sugar', 
          'https://www.alphavantage.co/query?function=SUGAR&interval=monthly',
          '68S617QRYKZHX4ZN')
df.to_csv('dfr_sugar.csv', index=False)  

df = create_df('corn', 
          'https://www.alphavantage.co/query?function=CORN&interval=monthly',
          '68S617QRYKZHX4ZN')
df.to_csv('df_corn.csv', index=False)  

df = create_df('wheat', 
          'https://www.alphavantage.co/query?function=WHEAT&interval=monthly',
          '68S617QRYKZHX4ZN')
df.to_csv('df_wheat.csv', index=False)  

df = create_df('index', 
          'https://www.alphavantage.co/query?function=ALL_COMMODITIES&interval=monthly',
          '68S617QRYKZHX4ZN')
df.to_csv('df_index.csv', index=False)  

'''
#_______________________________titre prevision_________________________________________________________________________________________


