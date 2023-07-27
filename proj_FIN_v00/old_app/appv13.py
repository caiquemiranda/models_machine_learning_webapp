import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

# Criando o gráfico de barras para o volume
volume = go.Bar(x=dados_acao.index,
                y=dados_acao['Volume'],
                name='Volume')

# Criando a figura com os gráficos de candles e volume
figura = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                       row_heights=[0.7, 0.3])

figura.add_trace(candlestick, row=1, col=1)
figura.add_trace(volume, row=2, col=1)

# Atualizando o layout do gráfico
figura.update_layout(title=f'Gráfico de Candles e Volume da Ação {acao}',
                     xaxis_title='Data',
                     yaxis_title='Preço',
                     xaxis_rangeslider_visible=False)

# Criando o aplicativo Flask
app = Flask(__name__)

# Rota para renderizar o template com o gráfico
@app.route('/')
def renderizar_grafico():
    return render_template('grafico_candles.html', acao=acao, plot=figura.to_html())

if __name__ == '__main__':
    app.run(debug=True)
