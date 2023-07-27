import yfinance as yf
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from ta.momentum import RSIIndicator

# Lista de ações para análise
acoes = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']

# Obtendo os dados históricos das ações
dados_acoes = yf.download(acoes, start='2022-01-01', end='2023-01-01')

# Verificar quais ações têm dados disponíveis
acoes_com_dados = dados_acoes.columns.get_level_values(0).unique()

# Filtrar apenas as ações com dados disponíveis
acoes_selecionadas = [acao for acao in acoes if acao in acoes_com_dados]

# Atualizar o DataFrame para conter apenas as ações selecionadas com dados disponíveis
df_selected_period = dados_acoes[acoes_selecionadas]

# Criando o aplicativo Flask com Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Resto do código continua o mesmo...

