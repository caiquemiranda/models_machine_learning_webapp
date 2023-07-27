import yfinance as yf
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# Ações para análise
acoes = ['AAPL', 'MSFT']

# Obtendo os dados históricos das ações
dados_acoes = yf.download(acoes, start='2022-01-01', end='2023-01-01')

# Criando o aplicativo Flask com Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do aplicativo
app.layout = html.Div([
    html.H1("Gráfico de Candles das Ações AAPL e MSFT"),
    dcc.Graph(id='candlestick-plot')
])

@app.callback(
    Output('candlestick-plot', 'figure'),
    [dash.dependencies.Input('candlestick-plot', 'relayoutData')]
)
def update_candlestick_plot(relayout_data):
    return {
        'data': [
            go.Candlestick(
                x=dados_acoes.index,
                open=dados_acoes[acao]['Open'],
                high=dados_acoes[acao]['High'],
                low=dados_acoes[acao]['Low'],
                close=dados_acoes[acao]['Adj Close'],
                name=acao
            )
            for acao in acoes
        ],
        'layout': {
            'title': 'Gráfico de Candles das Ações AAPL e MSFT',
            'xaxis': {'title': 'Data'},
            'yaxis': {'title': 'Preço de Fechamento'}
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)
