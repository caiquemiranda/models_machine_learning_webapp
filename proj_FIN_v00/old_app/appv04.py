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

# Renomear as colunas para que o nome da ação seja o nível superior das colunas
dados_acoes.columns = dados_acoes.columns.swaplevel(0, 1)
dados_acoes = dados_acoes[acoes]  # Filtrar apenas as ações selecionadas

# Criando o aplicativo Flask com Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


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


app.layout = html.Div([
    html.H1("Análise de Indicadores em Ações da Bolsa"),
    dcc.Graph(id='retorno-diario-plot'),
    dcc.Graph(id='correlacao-matrix-plot'),
    dcc.Graph(id='candlestick-plot'),
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
    ),
    dash_table.DataTable(
        id='precos-fechamento-tabela',
        columns=[{'name': col, 'id': col} for col in dados_acoes['Adj Close'].columns],
        data=dados_acoes['Adj Close'].reset_index().to_dict('records'),
        style_table={'overflowX': 'auto'}
    )
])

@app.callback(
    [Output('retorno-diario-plot', 'figure'),
     Output('correlacao-matrix-plot', 'figure'),
     Output('candlestick-plot', 'figure'),
     Output('estatisticas-tabela', 'children'),
     Output('precos-fechamento-tabela', 'data')],
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
            {'x': df_selected_period.index, 'y': df_selected_period[acao]['Adj Close'], 'name': acao}
            for acao in df_selected_period.columns.get_level_values(0)
        ],
        'layout': {
            'title': 'Retornos Diários das Ações Selecionadas',
            'xaxis': {'title': 'Data'},
            'yaxis': {'title': 'Retorno Diário'}
        }
    }

    # Cálculo e plot da matriz de correlação
    correlacao = df_selected_period['Adj Close'].pct_change().corr()
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
    estatisticas_df = df_selected_period['Adj Close'].pct_change().describe().transpose()
    estatisticas_tabela = [
        html.Tr([html.Th(acao)] + [html.Td(estatisticas_df.loc[acao][col]) for col in estatisticas_df.columns])
        for acao in estatisticas_df.index
    ]

    # Plot dos gráficos de candlestick
    candlestick_plot = {
        'data': [
            go.Candlestick(
                x=df_selected_period.index,
                open=df_selected_period[acao]['Open'],
                high=df_selected_period[acao]['High'],
                low=df_selected_period[acao]['Low'],
                close=df_selected_period[acao]['Adj Close'],
                name=acao
            )
            for acao in df_selected_period.columns.get_level_values(0)
        ],
        'layout': {
            'title': 'Gráfico de Candlestick',
            'xaxis': {'title': 'Data'},
            'yaxis': {'title': 'Preço de Fechamento'}
        }
    }

    # Atualização dos dados da tabela de preços de fechamento
    tabela_dados = df_selected_period['Adj Close'].reset_index().to_dict('records')

    return retorno_diario_plot, correlacao_matrix_plot, candlestick_plot, estatisticas_tabela, tabela_dados

if __name__ == '__main__':
    app.run_server(debug=True)
