from flask import Flask, render_template
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)

# Dados de exemplo (você pode substituí-los pelos seus próprios dados)
dados_exemplo = {
    'meses': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
    'vendas': [100, 150, 200, 120, 180]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grafico')
def gerar_grafico():
    meses = dados_exemplo['meses']
    vendas = dados_exemplo['vendas']

    # Criar o gráfico de barras
    grafico = go.Figure(data=[go.Bar(x=meses, y=vendas)])
    grafico.update_layout(title='Vendas por mês',
                          xaxis_title='Mês',
                          yaxis_title='Vendas')

    # Converter o gráfico para JSON para ser renderizado no frontend
    grafico_json = grafico.to_json()

    return render_template('grafico.html', grafico_json=grafico_json)

if __name__ == '__main__':
    app.run(debug=True)
