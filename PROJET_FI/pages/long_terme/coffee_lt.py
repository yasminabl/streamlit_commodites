import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from features.functions import *
from features.layout import *
from PIL import Image

# ___________________________________________ Import Data & Variables ___________________________________________

commodite = 'coffee'
df_coffee = pd.read_csv("df_coffee.csv", index_col=None)
df_index = pd.read_csv("df_index.csv", index_col=None)

# ___________________________________________ Clean Data ___________________________________________

df_coffee = clean_df(df_coffee, commodite)
df_index = clean_df(df_index, 'index')

# Debugging: Check the structure of df_index
if 'value_index' not in df_index.columns:
    st.error("The column 'value_index' is missing in df_index. Please verify the data source or cleaning process.")
    st.write("Columns in df_index:", df_index.columns)
    st.stop()

df_coffee_2 = df_coffee.copy()

# ___________________________________________ Title & Header ___________________________________________

picture = get_picture(commodite)
title = "Café : l’or brun sous la loupe des investisseurs"
subtitle = "Analyse approfondie des tendances, performances et métriques clés du marché du café"
display_header(picture, title, subtitle)


# ___________________________________________ Data Preparation ___________________________________________

# Reverse DataFrame order for visualization
reverse_dataframe(df_coffee)

# Combine coffee and index data
sub_df_coffee = pd.concat([df_coffee, df_index], axis=1)
sub_df_coffee_ind = sub_df_coffee.copy()

# Add indicators to the DataFrame
df_ind(sub_df_coffee_ind, commodite)

# ___________________________________________ Sidebar Filters ___________________________________________

selected_year_min, selected_month_min, selected_year_max, selected_month_max = get_date_range_from_sidebar(sub_df_coffee_ind)

# Filter data based on selected date range
sub_df_coffee_ind_filtered = filter_dataframe(
    sub_df_coffee_ind,
    selected_year_min,
    selected_month_min,
    selected_year_max,
    selected_month_max
)

selected_commodity = st.sidebar.radio(
    "Sélectionnez les cours à afficher",
    [commodite, 'Index', 'Les deux'],
    index=2
)

selected_indicators = st.sidebar.radio(
    "Sélectionnez les indicateurs à afficher",
    [f'MM_{commodite}', f'RSI_{commodite}', f'Stochastic_{commodite}']
)

# ___________________________________________ Display Data ___________________________________________

# Display descriptive statistics for coffee
display_custom_table(df_coffee, "Données descriptives sur le café")

# ___________________________________________ Generate Graphs ___________________________________________

fig1, title1 = graph_cours_boursier_long_term(sub_df_coffee_ind_filtered, selected_commodity, commodite)
fig2 = graph_indicateurs(sub_df_coffee_ind_filtered, commodite, selected_indicators)

display_graphs_long_term(
    fig1=fig1,
    title1="Graphique des cours à long terme",
    fig2=fig2,
    title2="Graphique des indicateurs techniques (long terme)",
    text_column_content="""
        <p style="text-align: justify;">
        Les graphiques ci-dessus montrent l'évolution à long terme des cours du café et des indices associés. 
        Les perspectives à long terme permettent de comprendre les cycles économiques et d'adapter les stratégies d'investissement.
        </p>
        <p style="text-align: justify;">
        Les indicateurs techniques offrent un aperçu supplémentaire sur les tendances sous-jacentes et la volatilité à long terme.
        </p>
    """
)