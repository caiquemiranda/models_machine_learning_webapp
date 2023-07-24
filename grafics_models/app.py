import dash
from dash import dcc, html
import plotly.graph_objs as go
import yfinance as yf

# Definir o ticker da ação (substitua "AAPL" pelo ticker da ação de sua escolha)
ticker = "AAPL"

# Obter dados financeiros da ação utilizando a biblioteca yfinance
dados_acao = yf.download(ticker, 
                         start="2022-01-01", 
                         end="2023-06-01")

# Inicializar a aplicação Dash
app = dash.Dash(__name__)

# Definir layout da aplicação
app.layout = html.Div([
    html.H1(f'Variação do Preço da Ação {ticker}'),
    dcc.Graph(
        id='grafico-acao',
        figure={
            'data': [
                go.Scatter(x=dados_acao.index, y=dados_acao['Close'], mode='lines', name='Preço de Fechamento')
            ],
            'layout': go.Layout(
                xaxis={'title': 'Data'},
                yaxis={'title': 'Preço de Fechamento'},
                hovermode='x'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
