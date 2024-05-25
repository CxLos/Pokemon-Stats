# IMPORTS -------------------------------------------------------------------
import csv, sqlite3
import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.graph_objects as go
import plotly.express as px
import datetime
import os
import sys
import dash
from dash import dcc, html
from dash.dependencies import Output, State
from dash.development.base_component import Component

# print('System Version:', sys.version)
# -------------------------------------------------- DATA -------------------------------------------------------

path = r'c:\Users\CxLos\OneDrive\Documents\Portfolio Projects\Pokemon-Stats\data\pokemon_data.csv'

# Get the current working directory
current_dir = os.getcwd()
# print('Current Directory:', current_dir)

# Join the 'Data' directory to the current working directory
imm_dir = os.path.join(current_dir, "Pokemon-Stats")

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
print('Script Directory:', script_dir)

# List the files and directories
# print('Dirctories List:', os.listdir(current_dir))
# print('Dirctories List:', os.listdir(script_dir))

# Define the relative path to your CSV file
relative_path = 'data/pokemon_data.csv'

# Join the script directory with the relative path to get the full file path
file_path = os.path.join(script_dir, relative_path)

# Read the CSV file using the full file path
# df = pd.read_csv(file_path)
df = pd.read_csv(path)

df.set_index('dexnum', inplace=True)

# print(df.head(10))
# print('Column Names:', df.columns)
# print('DF Shape:', df.shape)
# print('Dtypes:', df.dtypes)
# print('Amt of duplicate rows:', duplicate_len)
# print("Amount of duplicate rows:", df.duplicated().sum())

# Column Names ---------------------------------------------------------------

# Column Names: Index([
#        'dexnum', 'name', 'generation', 'type1', 'type2', 'species', 'height',
#        'weight', 'ability1', 'ability2', 'hidden_ability', 'hp', 'attack',
#        'defense', 'sp_atk', 'sp_def', 'speed', 'total', 'ev_yield',
#        'catch_rate', 'base_friendship', 'base_exp', 'growth_rate',
#        'egg_group1', 'egg_group2', 'percent_male', 'percent_female',
#        'egg_cycles', 'special_group']

# SQL---------------------------------------------------------------------------

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

df = pd.read_sql_query("""
  SELECT 
    'water' AS type,
    COUNT(*) AS count
  FROM pokemon_data 
  WHERE type1 ='Water' or type2 ='Water'
""", con)

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
  ORDER BY count DESC
""", con)

print(df_type_counts)

# print(df)
# print(df3)

con.close()
# ----------------------------------------------- DASHBOARD -------------------------------------------------

# Create dash application
# app = dash.Dash(__name__)
# server= app.server

# app.layout = html.Div(children=[ 

#             html.Div([
                
#                 html.H1('Pokemon Statistics', 
#                 className='title',
#                 style={
#                   # 'textAlign': 'center', 
#                   # 'color': 'cadetblue',
#                   # 'fontSize': 45, 
#                   # 'font-family':'Calibri', 
#                 # 'marginBottom':'5px'
#                 }),

#                 html.A(
#                 'Repo',
#                 href='https://github.com/CxLos/Pokemon-Stats',
#                 className='btn')
#                 ]),

            

#             # html.Br(),

#             # Row 1
#             html.Div(
#                 className='row1',
#                 children=[
#                       html.Div(
#                           className='graph1',
#                           children=[
#                               dcc.Graph( 
                                    
#                                     figure=px.bar(df.groupby('Year')['Immigrants Obtaining Lawful Permanent Resident Status'].sum().reset_index(), 
#                                         x='Year', y='Immigrants Obtaining Lawful Permanent Resident Status').
#                                         update_traces(line=dict(color='blue')).
#                                         update_layout(title='Immigrants Obtaining Lawful Permanent Resident Status', 
#                                     xaxis_title='Type', 
#                                     yaxis_title='Number of Pokemon',
#                                     title_x=0.5,
#                                     font=dict(
#                                           family='Calibri',  # Set the font family to Calibri
#                                           size=17,          # Adjust the font size as needed
#                                           color='black'))
#                                 )]),

            #           html.Div(
            #               className='graph2',
            #               children=[
            #                   dcc.Graph(
            #                         figure=px.line(df.groupby('Year')['Refugee Arrivals'].sum().reset_index(), 
            #                             x='Year', y='Refugee Arrivals').
            #                             update_traces(line=dict(color='red')).  # Change the line color
            #                             update_layout(title='Refugee Arrivals', 
            #                         xaxis_title='Year', 
            #                         yaxis_title='Refugee Arrivals',
            #                         title_x=0.5,
            #                         font=dict(
            #                               family='Calibri',  # Set the font family to Calibri
            #                               size=17,          # Adjust the font size as needed
            #                               color='black'))
            #                     )],
            #                     style={
            #                         # 'border':'2px solid black', 
            #                         #    'border-radius':'10px', 
            #                            'margin':'0px', 
            #                            'width':'48%'})], 
            #                     # style={'display': 'flex', 'textAlign': 'center'}
            #                     ),

            # # Row 2
            # html.Div(
            #     className='row2',
            #     children=[
            #           html.Div(className='graph3',
            #                    children=[
            #                  dcc.Graph(
            #               figure=px.line(df.groupby('Year')['Noncitizen Apprehensions'].sum().reset_index(), 
            #                   x='Year', y='Noncitizen Apprehensions').
            #                   update_traces(line=dict(color='green')).  # Change the line color
            #                   update_layout(title='Noncitizen Apprehensions', 
            #                xaxis_title='Year', 
            #                yaxis_title='Noncitizen Apprehensions',
            #                title_x=0.5,
            #                font=dict(
            #                     family='Calibri',  # Set the font family to Calibri
            #                     size=17,          # Adjust the font size as needed
            #                     color='black'))
            #           )],
            #           style={
            #             #   'border':'2px solid black', 
            #             #      'border-radius':'10px', 
            #                 #  'margin':'10px', 
            #                 #  'width':'49%'
            #                  }),

            #           html.Div(
            #               className='graph4',
            #               children=[
            #               dcc.Graph( 
            #               figure=px.line(df.groupby('Year')['Noncitizen Removals'].sum().reset_index(), 
            #                   x='Year', y='Noncitizen Removals').
            #                   update_traces(line=dict(color='orange')).  # Change the line color
            #                   update_layout(title='Noncitizen Removals', 
            #                xaxis_title='Year', 
            #                yaxis_title='Noncitizen Removals',
            #                title_x=0.5,
            #                font=dict(
            #                     family='Calibri',  # Set the font family to Calibri
            #                     size=17,          # Adjust the font size as needed
            #                     color='black'))
            #           )],
            #           style={
            #             #   'border':'2px solid black', 
            #             #      'border-radius':'10px', 
            #                 #  'margin':'0px', 
            #                 #  'width':'48%'
            #                  })], 
            #           style={'display': 'flex', 'textAlign': 'center'})
            # ])

# Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True, 
#                   #  port=8055
#                    )

#  KILL PORT --------------------------------------------

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

# Heroku Setup:
# heroku login
# heroku create cxlos-pokemon-stats
# heroku git:remote -a cxlos-pokemon-stats
# git push heroku main

# Clear Heroku Cache:
# heroku plugins:install heroku-repo
# heroku repo:purge_cache -a pokemon-stats