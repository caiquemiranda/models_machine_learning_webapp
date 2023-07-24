import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import yfinance as yf
import dash_bootstrap_components as dbc

# Lista de tickers das ações disponíveis
acoes_disponiveis = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB']

# Função para obter os dados financeiros de uma ação
def obter_dados_acao(ticker):
    dados_acao = yf.download(ticker, start="2022-01-01", end="2023-01-01")
    return dados_acao

# Função para criar o gráfico de candlesticks
def criar_grafico_candlestick(dados_acao, ticker):
    grafico = go.Figure(data=[go.Candlestick(x=dados_acao.index,
                                            open=dados_acao['Open'],
                                            high=dados_acao['High'],
                                            low=dados_acao['Low'],
                                            close=dados_acao['Close'])])

    grafico.update_layout(
        title=f'Gráfico de Candlesticks - Ação {ticker}',
        xaxis_title='Data',
        yaxis_title='Preço',
        template='plotly_dark'  # Utilizar o tema "Slate"
    )
    
    return grafico

# Função para criar o gráfico de linha
def criar_grafico_linha(dados_acao, ticker):
    grafico = go.Figure(data=[go.Scatter(x=dados_acao.index, y=dados_acao['Close'], mode='lines', name='Preço de Fechamento')])

    grafico.update_layout(
        title=f'Gráfico de Linha - Ação {ticker}',
        xaxis_title='Data',
        yaxis_title='Preço de Fechamento',
        template='plotly_dark'  # Utilizar o tema "Slate"
    )
    
    return grafico

# Inicializar a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Definir layout da aplicação
app.layout = dbc.Container([
    html.H1(children='Gráficos Financeiros', className='title is-1', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='dropdown-acoes',
        options=[{'label': ticker, 'value': ticker} for ticker in acoes_disponiveis],
        value='AAPL'
    ),
    dcc.Dropdown(
        id='dropdown-graficos',
        options=[
            {'label': 'Candlesticks', 'value': 'candlestick'},
            {'label': 'Linha', 'value': 'linha'}
        ],
        value='candlestick',
        style={'margin-top': '10px'}
    ),
    dcc.Graph(id='grafico')
])

# Definir callback para atualizar o gráfico de acordo com a ação e tipo de gráfico selecionado
@app.callback(Output('grafico', 'figure'),
              [Input('dropdown-acoes', 'value'),
               Input('dropdown-graficos', 'value')])
def atualizar_grafico(ticker_selecionado, tipo_grafico):
    dados_acao = obter_dados_acao(ticker_selecionado)
    
    if tipo_grafico == 'candlestick':
        grafico = criar_grafico_candlestick(dados_acao, ticker_selecionado)
    elif tipo_grafico == 'linha':
        grafico = criar_grafico_linha(dados_acao, ticker_selecionado)
    else:
        grafico = go.Figure()

    return grafico

if __name__ == '__main__':
    app.run_server(debug=True)
