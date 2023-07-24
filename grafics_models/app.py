import dash
from dash import dcc, html
import plotly.graph_objs as go

# Dados de exemplo atualizados
dados_exemplo = {
    'meses': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
    'vendas_produto_a': [100, 120, 90, 150, 80],
    'vendas_produto_b': [80, 100, 110, 90, 120]
}

# Inicializar a aplicação Dash
app = dash.Dash(__name__)

# Definir layout da aplicação
app.layout = html.Div([
    html.H1('Gráfico de Vendas por Mês - Produto A vs Produto B'),
    dcc.Graph(
        id='grafico-vendas',
        figure={
            'data': [
                go.Bar(x=dados_exemplo['meses'], y=dados_exemplo['vendas_produto_a'], name='Produto A'),
                go.Bar(x=dados_exemplo['meses'], y=dados_exemplo['vendas_produto_b'], name='Produto B')
            ],
            'layout': go.Layout(
                xaxis={'title': 'Mês'},
                yaxis={'title': 'Vendas'},
                barmode='stack'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
