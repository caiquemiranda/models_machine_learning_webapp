from flask import Flask, render_template
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)
"""
# Dados de exemplo (você pode substituí-los pelos seus próprios dados)
dados_exemplo = {
    'meses': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
    'vendas': [100, 150, 200, 120, 180]
}
"""

# Dados de exemplo atualizados
dados_exemplo = {
    'meses': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
    'vendas_produto_a': [100, 120, 90, 150, 80],
    'vendas_produto_b': [80, 100, 110, 90, 120]
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grafico')
@app.route('/grafico')
def gerar_grafico():
    meses = dados_exemplo['meses']
    vendas_produto_a = dados_exemplo['vendas_produto_a']
    vendas_produto_b = dados_exemplo['vendas_produto_b']

    # Criar o gráfico de barras empilhadas
    grafico = go.Figure()
    grafico.add_trace(go.Bar(x=meses, y=vendas_produto_a, name='Produto A'))
    grafico.add_trace(go.Bar(x=meses, y=vendas_produto_b, name='Produto B'))

    grafico.update_layout(title='Vendas por mês - Produto A vs Produto B',
                          xaxis_title='Mês',
                          yaxis_title='Vendas',
                          barmode='stack')

    # Converter o gráfico para JSON para ser renderizado no frontend
    grafico_json = grafico.to_json()

    return render_template('grafico.html', grafico_json=grafico_json)

if __name__ == '__main__':
    app.run(debug=True)
