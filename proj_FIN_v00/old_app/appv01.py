import yfinance as yf
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Lista de ações para análise
acoes = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']

# Obtendo os dados históricos das ações
dados_acoes = yf.download(acoes, start='2022-01-01', end='2023-01-01')['Adj Close']

# Calculando os retornos diários das ações
retorno_diario = dados_acoes.pct_change()

# Criando o aplicativo Flask com Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Análise de Indicadores em Ações da Bolsa"),
    dcc.Graph(id='retorno-diario-plot'),
    dcc.Graph(id='correlacao-matrix-plot'),
    html.Hr(),
    html.H3("Estatísticas Básicas dos Retornos"),
    html.Table(id='estatisticas-tabela'),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=dados_acoes.index.min(),
        end_date=dados_acoes.index.max(),
        display_format='DD/MM/YYYY'
    ),
    dcc.Dropdown(
        id='acoes-dropdown',
        options=[{'label': acao, 'value': acao} for acao in acoes],
        value=acoes,
        multi=True
    )
])

@app.callback(
    [Output('retorno-diario-plot', 'figure'),
     Output('correlacao-matrix-plot', 'figure'),
     Output('estatisticas-tabela', 'children')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('acoes-dropdown', 'value')]
)
def update_graph(start_date, end_date, acoes_selecionadas):
    df_selected_period = dados_acoes.loc[start_date:end_date]

    # Filtrando as ações selecionadas
    df_selected_period = df_selected_period[acoes_selecionadas]

    # Plot dos retornos diários
    retorno_diario_plot = {
        'data': [
            {'x': df_selected_period.index, 'y': df_selected_period[acao], 'name': acao}
            for acao in df_selected_period.columns
        ],
        'layout': {
            'title': 'Retornos Diários das Ações Selecionadas',
            'xaxis': {'title': 'Data'},
            'yaxis': {'title': 'Retorno Diário'}
        }
    }

    # Cálculo e plot da matriz de correlação
    correlacao = df_selected_period.pct_change().corr()
    correlacao_matrix_plot = {
        'data': [
            {
                'z': correlacao.values.tolist(),
                'x': acoes_selecionadas,
                'y': acoes_selecionadas,
                'type': 'heatmap',
                'colorscale': 'Viridis',
            }
        ],
        'layout': {
            'title': 'Matriz de Correlação entre as Ações Selecionadas'
        }
    }

    # Cálculo das estatísticas básicas
    estatisticas_df = df_selected_period.pct_change().describe().transpose()
    estatisticas_tabela = [
        html.Tr([html.Th(acao)] + [html.Td(estatisticas_df.loc[acao][col]) for col in estatisticas_df.columns])
        for acao in estatisticas_df.index
    ]

    return retorno_diario_plot, correlacao_matrix_plot, estatisticas_tabela

if __name__ == '__main__':
    app.run_server(debug=True)
