import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import yfinance as yf
import dash_bootstrap_components as dbc

# Definir o ticker da ação (substitua "AAPL" pelo ticker da ação de sua escolha)
ticker = "AAPL"

# Obter dados financeiros da ação utilizando a biblioteca yfinance
dados_acao = yf.download(ticker, start="2022-01-01", end="2023-01-01")

# Criar o gráfico de candlesticks
grafico_candlestick = go.Figure(data=[go.Candlestick(x=dados_acao.index,
                                                    open=dados_acao['Open'],
                                                    high=dados_acao['High'],
                                                    low=dados_acao['Low'],
                                                    close=dados_acao['Close'])])

# Personalizar o layout do gráfico
grafico_candlestick.update_layout(
    title=f'Gráfico de Candlesticks - Ação {ticker}',
    xaxis_title='Data',
    yaxis_title='Preço',
    template='plotly_dark'  # Utilizar o tema "Slate"
)

# Inicializar a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BULMA])

# Definir layout da aplicação
app.layout = dbc.Container([
    html.H1(children=f'Gráfico de Candlesticks - Ação {ticker}', className='title is-1', style={'textAlign': 'center'}),
    dcc.Graph(
        id='grafico-candlestick',
        figure=grafico_candlestick
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
