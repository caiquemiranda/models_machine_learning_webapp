import yfinance as yf
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output  # Importação corrigida

# Lista de ações para análise
acoes = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']

# Obtendo os dados históricos das ações
dados_acoes = yf.download(acoes, start='2023-01-01', end='2023-03-01')

# Renomear as colunas para que o nome da ação seja o nível superior das colunas
dados_acoes.columns = dados_acoes.columns.swaplevel(0, 1)
dados_acoes = dados_acoes[acoes]  # Filtrar apenas as ações selecionadas

# Criando o aplicativo Flask com Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do aplicativo
app.layout = html.Div([
    html.H1("Gráfico de Candles das Ações Selecionadas"),
    dcc.Graph(id='candlestick-plot')
])

@app.callback(
    Output('candlestick-plot', 'figure'),
    [Input('candlestick-plot', 'relayoutData')]
)
def update_candlestick_plot(relayout_data):
    # Apenas para demonstrar que podemos atualizar o gráfico com novos dados de acordo com o relayoutData
    # Mas não é necessário para o gráfico de candles simples
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
            for acao in dados_acoes.columns.get_level_values(0)
        ],
        'layout': {
            'title': 'Gráfico de Candles das Ações Selecionadas',
            'xaxis': {'title': 'Data'},
            'yaxis': {'title': 'Preço de Fechamento'}
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)
