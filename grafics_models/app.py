import dash
from dash import dcc, html
import plotly.graph_objs as go
import yfinance as yf

# Definir o ticker da ação (substitua "AAPL" pelo ticker da ação de sua escolha)
ticker = "AAPL"

# Obter dados financeiros da ação utilizando a biblioteca yfinance
dados_acao = yf.download(ticker, 
                         start="2023-04-01", 
                         end="2023-06-01")

# Criar o gráfico de candlesticks
grafico_candlestick = go.Figure(data=[go.Candlestick(x=dados_acao.index,
                                                    open=dados_acao['Open'],
                                                    high=dados_acao['High'],
                                                    low=dados_acao['Low'],
                                                    close=dados_acao['Close'])])

# Inicializar a aplicação Dash
app = dash.Dash(__name__)

# Definir layout da aplicação
app.layout = html.Div([
    html.H1(f'Gráfico de Candlesticks - Ação {ticker}'),
    dcc.Graph(
        id='grafico-candlestick',
        figure=grafico_candlestick
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
