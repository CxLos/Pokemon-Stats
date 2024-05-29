# IMPORTS -------------------------------------------------------------------
import csv, sqlite3
import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
import datetime
import os
import sys
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.development.base_component import Component

# print('System Version:', sys.version)
# -------------------------------------------------- DATA -------------------------------------------------------

# path = r'c:\Users\CxLos\OneDrive\Documents\Portfolio Projects\Pokemon-Stats\data\pokemon_data.csv'

# Get the current working directory
current_dir = os.getcwd()
# print('Current Directory:', current_dir)

# Join the 'Data' directory to the current working directory
imm_dir = os.path.join(current_dir, "Pokemon-Stats")

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
# print('Script Directory:', script_dir)

# List the files and directories
# print('Dirctories List:', os.listdir(current_dir))
# print('Dirctories List:', os.listdir(script_dir))

# Define the relative path to your CSV file
relative_path = 'data/pokemon_data.csv'

# Join the script directory with the relative path to get the full file path
file_path = os.path.join(script_dir, relative_path)

# Read the CSV file using the full file path
df = pd.read_csv(file_path)
# df = pd.read_csv(path)

df.set_index('dexnum', inplace=True)

# Rename Columns
df['generation'] = df['generation'].replace(1, 'Kanto')
df['generation'] = df['generation'].replace(2, 'Johto')
df['generation'] = df['generation'].replace(3, 'Hoenn')
df['generation'] = df['generation'].replace(4, 'Sinnoh')
df['generation'] = df['generation'].replace(5, 'Unova')
df['generation'] = df['generation'].replace(6, 'Kalos')
df['generation'] = df['generation'].replace(7, 'Alola')
df['generation'] = df['generation'].replace(8, 'Galar')
df['generation'] = df['generation'].replace(9, 'Paldea')

# print(df.head(10))
# print('Total # o Pokemon: ', len(df))
# print('Column Names:', df.columns)
# print('DF Shape:', df.shape)
# print('Dtypes:', df.dtypes)
# print('Amt of duplicate rows:', duplicate_len)
# print("Amount of duplicate rows:", df.duplicated().sum())

# ---------------------------------------------- Column Names ------------------------------------------------------

# Column Names: Index([
#        'dexnum', 'name', 'generation', 'type1', 'type2', 'species', 'height',
#        'weight', 'ability1', 'ability2', 'hidden_ability', 'hp', 'attack',
#        'defense', 'sp_atk', 'sp_def', 'speed', 'total', 'ev_yield',
#        'catch_rate', 'base_friendship', 'base_exp', 'growth_rate',
#        'egg_group1', 'egg_group2', 'percent_male', 'percent_female',
#        'egg_cycles', 'special_group']

# --------------------------------------------- Pokemon Types -----------------------------------------------------

# Get the distinct values in column 'type1'
# distinct_types = df['type1'].unique()
# print('Pokemon Types:\n', distinct_types)

# ['Grass' 'Fire' 'Water' 'Bug' 'Normal' 'Poison' 'Electric' 'Ground'
#  'Fairy' 'Fighting' 'Psychic' 'Rock' 'Ghost' 'Ice' 'Dragon' 'Dark' 'Steel'
#  'Flying']

# --------------------------------------------------- SQL ----------------------------------------------------------

# Connect to SQL
con = sqlite3.connect("pokemon.db")
cur = con.cursor()

df.to_sql("pokemon_data", con, if_exists='replace', index=False, method="multi")

# Show list of all tables in db.
tables = pd.read_sql_query("""
  SELECT name 
  FROM sqlite_master 
  WHERE type = 'table';
""", con)
# print("Tables in the database:\n", tables)

# Check if data is inserted correctly
df_check = pd.read_sql_query("SELECT * FROM pokemon_data LIMIT 5;", con)
# print("Data in DB:\n", df_check)

# All Pokemon Types
df_unique_types = pd.read_sql_query("""
  SELECT DISTINCT type1 
  FROM pokemon_data;
""", con)
# print("Pokemon Types::\n", df_unique_types)

# df = pd.read_sql_query("""
#   select name, type1, type2, ability1 from pokemon_data limit 9;
# """, con)

# 1. Bar Chart Number of Pokemon by Type
df_type_counts = pd.read_sql_query("""
  SELECT 
    'Grass' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Grass' OR type2 = 'Grass'
  UNION ALL
  SELECT 
    'Fire' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Fire' OR type2 = 'Fire'
  UNION ALL
  SELECT 
    'Water' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Water' OR type2 = 'Water'
  UNION ALL
  SELECT 
    'Bug' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Bug' OR type2 = 'Bug'
  UNION ALL
  SELECT 
    'Normal' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Normal' OR type2 = 'Normal'
  UNION ALL
  SELECT 
    'Poison' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Poison' OR type2 = 'Poison'
  UNION ALL
  SELECT 
    'Electric' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Electric' OR type2 = 'Electric'
  UNION ALL
  SELECT 
    'Ground' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Ground' OR type2 = 'Ground'
  UNION ALL
  SELECT 
    'Fairy' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Fairy' OR type2 = 'Fairy'
  UNION ALL
  SELECT 
    'Fighting' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Fighting' OR type2 = 'Fighting'
  UNION ALL
  SELECT 
    'Psychic' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Psychic' OR type2 = 'Psychic'
  UNION ALL
  SELECT 
    'Rock' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Rock' OR type2 = 'Rock'
  UNION ALL
  SELECT 
    'Ghost' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Ghost' OR type2 = 'Ghost'
  UNION ALL
  SELECT 
    'Ice' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Ice' OR type2 = 'Ice'
  UNION ALL
  SELECT 
    'Dragon' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Dragon' OR type2 = 'Dragon'
  UNION ALL
  SELECT 
    'Dark' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Dark' OR type2 = 'Dark'
  UNION ALL
  SELECT 
    'Steel' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Steel' OR type2 = 'Steel'
  UNION ALL
  SELECT 
    'Flying' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 = 'Flying' OR type2 = 'Flying'
""", con)

# Define custom colors for each type
colors = {
    'Grass': '#78C850',
    'Fire': '#F08030',
    'Water': '#6890F0',
    'Bug': '#A8B820',
    'Normal': '#A8A878',
    'Poison': '#A040A0',
    'Electric': '#F8D030',
    'Ground': '#E0C068',
    'Fairy': '#EE99AC',
    'Fighting': '#C03028',
    'Psychic': '#F85888',
    'Rock': '#B8A038',
    'Ghost': '#705898',
    'Ice': '#98D8D8',
    'Dragon': '#7038F8',
    'Dark': '#705848',
    'Steel': '#B8B8D0',
    'Flying': '#A890F0'
}


# 2. Pie Chart Number of Pokemon Introduced by Generation
# Generations
gen_list = pd.read_sql_query("""
  SELECT DISTINCT generation
  FROM pokemon_data
""", con)
# print(gen_list)

gen_counts = pd.read_sql_query("""
  SELECT 
    'Kanto' AS generation,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE generation = 'Kanto'
  UNION ALL
  SELECT 
    'Johto' AS generation,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE generation = 'Johto'
  UNION ALL
  SELECT 
    'Hoenn' AS generation,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE generation = 'Hoenn'
  UNION ALL
  SELECT 
    'Sinnoh' AS generation,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE generation = 'Sinnoh'
  UNION ALL
  SELECT 
    'Unova' AS generation,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE generation = 'Unova'
  UNION ALL
  SELECT 
    'Kalos' AS generation,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE generation = 'Kalos'
  UNION ALL
  SELECT 
    'Alola' AS generation,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE generation = 'Alola'
  UNION ALL
  SELECT 
    'Galar' AS generation,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE generation = 'Galar'
  UNION ALL
  SELECT 
    'Paldea' AS generation,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE generation = 'Paldea'
  ORDER BY count DESC
""", con)
# print(gen_counts)

# Gender Distribution
gender_query = pd.read_sql_query("""
  SELECT 
    100.0 as male_only,
    COUNT(*) as count
  FROM pokemon_data
  WHERE percent_male = 100
  UNION
  SELECT 
    100.0 as female_only,
    COUNT(*) as count
  FROM pokemon_data
  WHERE percent_female = 100

""", con)

# Heatmap

# 4. Heatmap figure base stat correlation

# Correlation matrix
corr = df[['hp', 'attack', 'defense', 'sp_atk', 'sp_def', 'speed', 'total']].corr()
# print(corr)

# Figure
heatmap_fig = ff.create_annotated_heatmap(
    z=corr.values,
    x=list(corr.columns),
    y=list(corr.index),
    colorscale='RdBu',
    annotation_text=corr.round(2).values,
    showscale=True
)

heatmap_fig.update_layout(
    title='Correlation Matrix of Base Stats',
    title_x=0.5,
    font=dict(
        family='Calibri',  # Set the font family to Calibri
        size=17,  # Adjust the font size as needed
        color='black'
    )
)

# 5. box plot total stats by generation
box_plot_fig = px.box(df, x='generation', y='total', points='all', color='generation', title='Box Plot of Total Stats by Generation')
box_plot_fig.update_layout(
    title='Box Plot of Total Stats by Generation',
    title_x=0.5,
    font=dict(
        family='Calibri',  # Set the font family to Calibri
        size=17,  # Adjust the font size as needed
        color='black'
    ),
    xaxis_title='Generation',
    yaxis_title='Total Stats'
)

# 6. average stats by generation figure
# avg_stats_by_gen = df.groupby('generation').mean().reset_index()
# avg_stats_fig = px.bar(avg_stats_by_gen, x='generation', y='total', title='Average Total Stats by Generation')
# avg_stats_fig.update_layout(
#     title='Average Total Stats by Generation',
#     title_x=0.5,
#     font=dict(
#         family='Calibri',  # Set the font family to Calibri
#         size=17,  # Adjust the font size as needed
#         color='black'
#     ),
#     xaxis_title='Generation',
#     yaxis_title='Average Total Stats'
# )

# print(df)
# print(df3)

con.close()
# ----------------------------------------------- DASHBOARD -------------------------------------------------

app = dash.Dash(__name__)
server= app.server

app.layout = html.Div(children=[ 

    html.Div(className='divv', children=[ 
        
        html.H1('Pokemon Statistics', 
        className='title'),

        html.A(
        'Repo',
        href='https://github.com/CxLos/Pokemon-Stats',
        className='btn')
        ]),

# ROW 1

html.Div(
    className='row1',
    children=[

        html.Div(
            className='graph1',
            children=[
                dcc.Graph(
                id='type-bar-chart',  # Add an id to the Graph
                figure=px.bar(
                    df_type_counts,
                    x='type', y='count', color = 'type', color_discrete_map=colors
                ).update_layout(
                    title='Number of Pokemon by Type',
                    xaxis_title='Type',
                    yaxis_title='Number of Pokemon',
                    title_x=0.5,
                    font=dict(
                        family='Calibri',  # Set the font family to Calibri
                        size=17,  # Adjust the font size as needed
                        color='black'
                    )
                )
            )
            ]
        ),

        html.Div(
            className='graph2',
            children=[
            #      dcc.Graph(
            #         id='gen-pie-chart', 
            #         figure=px.pie(
            #             gen_counts,
            #             names = 'generation',
            #             values = 'count',
            #             title = 'Number of Pokemon Introduced by Generation'
            #         ).update_layout(
            #             title='Number of Pokemon Introduced by Generation',
            #             title_x=0.5,
            #             font=dict(
            #                 family='Calibri',  # Set the font family to Calibri
            #                 size=17,  # Adjust the font size as needed
            #                 color='black'
            #         )
            #     )
            # )
                    dcc.Graph(
                        id='gen-bar-chart',  # Changed id to reflect the new chart type
                        figure=px.bar(
                            gen_counts,
                            x='count',
                            y='generation',
                            orientation='h',  # Set the orientation to horizontal
                            title='Number of Pokemon Introduced by Generation',
                            color='generation',  # Optional: color by generation for better visualization
                            color_discrete_sequence=px.colors.qualitative.Safe  # Optional: change color palette
                        ).update_layout(
                            title='Number of Pokemon Introduced by Generation',
                            title_x=0.5,
                            font=dict(
                                family='Calibri',  # Set the font family to Calibri
                                size=17,  # Adjust the font size as needed
                                color='black'
                            ),
                            xaxis_title='Number of Pokemon',
                            yaxis_title='Generation'
                        )
                    )
            ]
        )
    ]
),

# ROW 2

html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
               html.H1('Total Number of Pokemon', className='pkmntotal'),
               html.H2('1,025', className='count')
            ]
        ),

        html.Div(
            className='graph4',
            children=[
                         dcc.Graph(
                    id='tchart',  # Add an id to the Graph
                    figure=ff.create_annotated_heatmap(
                        z=corr.values,
                        x=list(corr.columns),
                        y=list(corr.index),
                        colorscale='Viridis',
                        annotation_text=corr.round(2).values,
                        showscale=True
                    ).update_layout(
                        title='Correlation Matrix of Base Stats',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',  # Set the font family to Calibri
                            size=17,  # Adjust the font size as needed
                            color='black'
                        )
                    )
                )
            ]
        )
    ]
),

# ROW 3

html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph5',
            children=[
                dcc.Graph(
                    id='box-plot',
                    figure=box_plot_fig
                )
            ]
        ),

        html.Div(
            className='graph6',
            children=[
                # dcc.Graph(
                    # id='avg-stats',
                    # figure=avg_stats_fig
                # )
            ]
        )
    ]
)
])

# callback to update the bar chart
# @app.callback([
#     Output('type-bar-chart', 'figure')],
#     [Input('type-bar-chart', 'id')])    

# Graphs
def update_bar_chart(_):
    fig = px.bar(df_type_counts, x='type', y='count',
                 title='Count of Each Pokémon Type',
                 labels={'type': 'Type', 'count': 'Count'})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, 
                  #  port=8056
                   )

# ------------------------------------------------- KILL PORT -----------------------------------------------------

# netstat -ano | findstr :8050
# taskkill /PID 24772 /F
# npx kill-port 8050

# ---------------------------------------------- Host Application ------------------------------------------------

# 1. pip freeze > requirements.txt
# 2. add this to procfile: 'web: gunicorn pokemon:server'
# 3. heroku login
# 4. heroku create
# 5. git push heroku main

# Create venv 
# virtualenv venv # creates a virtualenv called "venv"
# source venv/bin/activate # uses the virtualenv

# Update PIP Setup Tools:
# pip install --upgrade pip setuptools

# Install all dependencies in the requirements file:
# pip install -r requirements.txt

# Check dependency tree:
# pipdeptree
# pip show package-name

# Remove
# pypiwin32
# jupytercore

# Heroku Setup:
# heroku login
# heroku create cxlos-pokemon-stats
# heroku git:remote -a cxlos-pokemon-stats
# git push heroku main

# Clear Heroku Cache:
# heroku plugins:install heroku-repo
# heroku repo:purge_cache -a pokemon-stats

# Set buildpack for heroku
# heroku buildpacks:set heroku/python