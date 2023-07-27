import yfinance as yf
import plotly.graph_objects as go
from flask import Flask, render_template

# Ação para análise
acao = 'AAPL'  # Altere para a ação desejada

# Obtendo os dados históricos da ação
dados_acao = yf.download(acao, start='2022-01-01', end='2023-01-01')

# Criando o gráfico de candles
candlestick = go.Candlestick(x=dados_acao.index,
                             open=dados_acao['Open'],
                             high=dados_acao['High'],
                             low=dados_acao['Low'],
                             close=dados_acao['Close'],
                             name=acao)

# Layout do gráfico
layout = go.Layout(title=f'Gráfico de Candles da Ação {acao}',
                   xaxis=dict(title='Data'),
                   yaxis=dict(title='Preço'))

# Criando a figura com o gráfico de candles
figura = go.Figure(data=[candlestick], layout=layout)

# Criando o aplicativo Flask
app = Flask(__name__)

# Rota para renderizar o template com o gráfico
@app.route('/')
def renderizar_grafico():
    return render_template('grafico_candles.html', acao=acao, plot=figura.to_html())

if __name__ == '__main__':
    app.run(debug=True)
