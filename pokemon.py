# IMPORTS -------------------------------------------------------------------
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

print('System Version:', sys.version)

# -------------------------------------------------- DATA -------------------------------------------------------

# Get the current working directory
current_dir = os.getcwd()
print('Current Directory:', current_dir)

# Join the 'Data' directory to the current working directory
imm_dir = os.path.join(current_dir, "Pokemon-Stats")

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
print('Script Directory:', script_dir)

# List the files and directories
# print('Dirctories List:', os.listdir(current_dir))
print('Dirctories List:', os.listdir(script_dir))

# Define the relative path to your CSV file
relative_path = 'data/pokemon_data.csv'

# Join the script directory with the relative path to get the full file path
file_path = os.path.join(script_dir, relative_path)

# Read the CSV file using the full file path
df = pd.read_csv(file_path)

print(df.head(10))
print('Column Names:', df.columns)
print('DF Shape:', df.shape)
print('Dtypes:', df.dtypes)
# print('Amt of duplicate rows:', duplicate_len)

# ---------------------------------------------------------------------------

# ----------------------------------------------- DASHBOARD -------------------------------------------------

# Create dash application
app = dash.Dash(__name__)
server= app.server

app.layout = html.Div(children=[ 

            # html.Div([
                
            #     html.H1('US Immigration Statistics', 
            #     className='title',
            #     style={'textAlign': 'center', 
            #            'color': 'cadetblue',
            #     'fontSize': 45, 
            #     'font-family':'Calibri', 
            #     # 'marginBottom':'5px'
            #     }),

            #     html.A(
            #     'Repo',
            #     href='https://github.com/CxLos/US_Immigration_Statistics',
            #     className='btn')],
            #     style={'display': 'flex', 
            #             'flexDirection':'column',
            #             'textAlign': 'center', 
            #             'margin':'0px'}
            # ),

            

            # # html.Br(),

            # # Row 1
            # html.Div(
            #     className='row1',
            #     children=[
            #           html.Div(
            #               className='graph1',
            #               children=[
            #                   dcc.Graph( 
                                    
            #                         figure=px.line(df.groupby('Year')['Immigrants Obtaining Lawful Permanent Resident Status'].sum().reset_index(), 
            #                             x='Year', y='Immigrants Obtaining Lawful Permanent Resident Status').
            #                             update_traces(line=dict(color='blue')).  # Change the line color
            #                             update_layout(title='Immigrants Obtaining Lawful Permanent Resident Status', 
            #                         xaxis_title='Year', 
            #                         yaxis_title='Number of Immigrants',
            #                         title_x=0.5,
            #                         font=dict(
            #                               family='Calibri',  # Set the font family to Calibri
            #                               size=17,          # Adjust the font size as needed
            #                               color='black'))
            #                     ), 
            #                     html.P(
            #                       "This line chart illustrates the number of immigrants who obtained lawful permanent resident status in the United States over the years. The upward or downward trends can indicate the effects of policy changes, economic factors, and global events on immigration.",
            #                       style={
            #                           'textAlign': 'justify',
            #                           'margin': '20px',
            #                           'font-family': 'Calibri', 
            #                           'fontSize': '17px',        
            #                           'color': 'black'          
            #                       })],

            #                     style={
            #                         # 'border':'2px solid black', 
            #                         #    'border-radius':'10px', 
            #                         #    'margin':'0px', 
            #                         #    'width':'48%', 
            #                         #    'padding':'10px'
            #                            }),

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
            #                     ), 
            #                     html.P(
            #                       "This line chart illustrates the number of Refugee in the United States over the years. The peak in immigration in 1980 could most likely be attributed to refugees primarily from Vietnam, Cambodia, and Laos as the US allowed them into the country after the Vietnam War.",
            #                       style={
            #                           'textAlign': 'justify',
            #                           'margin': '20px',
            #                           'font-family': 'Calibri', 
            #                           'fontSize': '17px',        
            #                           'color': 'black' })],
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
            #           ), 
            #           html.P(
            #             "This line chart illustrates the trend in noncitizen apprehensions over the years. Noncitizen apprehensions refer to instances where individuals without citizenship status are detained or arrested. Understanding the trends in apprehensions can provide insights into changes in immigration enforcement, border security, and migration patterns. Factors influencing these trends may include shifts in immigration policies, socio-economic conditions, and geopolitical events.",
            #             style={
            #                 'textAlign': 'justify',
            #                 'margin': '20px',
            #                 'font-family': 'Calibri', 
            #                 'fontSize': '17px',        
            #                 'color': 'black' })],
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
            #           ), 
            #           html.P(
            #             "This line chart illustrates the trend in non-citizen removals over the years. Non-citizen removals refer to instances where individuals without citizenship status are deported or expelled from the country. Understanding the trends in removals can provide insights into changes in immigration enforcement, deportation policies, and migration patterns. Factors influencing these trends may include shifts in immigration laws, diplomatic relations, and international agreements.",
            #             style={
            #                 'textAlign': 'justify',
            #                 'margin': '20px',
            #                 'font-family': 'Calibri', 
            #                 'fontSize': '17px',        
            #                 'color': 'black' })],
            #           style={
            #             #   'border':'2px solid black', 
            #             #      'border-radius':'10px', 
            #                 #  'margin':'0px', 
            #                 #  'width':'48%'
            #                  })], 
            #           style={'display': 'flex', 'textAlign': 'center'})
            ])

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
# heroku create pokemon-stats
# heroku git:remote -a pokemon-stats
# git push heroku main

# Clear Heroku Cache:
# heroku plugins:install heroku-repo
# heroku repo:purge_cache -a pokemon-stats