import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from flask import Flask, render_template

# Ação para análise
acao = 'AAPL'  # Altere para a ação desejada

# Obtendo os dados históricos da ação
dados_acao = yf.download(acao, start='2022-01-01', end='2023-01-01')

# Calculando as médias móveis de 9 e 21 períodos
dados_acao['MA9'] = dados_acao['Close'].rolling(window=9).mean()
dados_acao['MA21'] = dados_acao['Close'].rolling(window=21).mean()

# Criando o gráfico de candles
candlestick = go.Candlestick(x=dados_acao.index,
                             open=dados_acao['Open'],
                             high=dados_acao['High'],
                             low=dados_acao['Low'],
                             close=dados_acao['Close'],
                             name=acao)

# Criando as linhas para as médias móveis
ma9 = go.Scatter(x=dados_acao.index, y=dados_acao['MA9'], line=dict(color='blue', width=1.5), name='MA9')
ma21 = go.Scatter(x=dados_acao.index, y=dados_acao['MA21'], line=dict(color='orange', width=1.5), name='MA21')

# Criando a figura com os gráficos de candles, volume e médias móveis
figura = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                       row_heights=[0.5, 0.2, 0.2])

figura.add_trace(candlestick, row=1, col=1)
figura.add_trace(volume, row=2, col=1)
figura.add_trace(ma9, row=1, col=1)
figura.add_trace(ma21, row=1, col=1)

# Atualizando o layout do gráfico
figura.update_layout(title=f'Gráfico de Candles, Volume e Médias Móveis da Ação {acao}',
                     xaxis_title='Data',
                     xaxis_rangeslider_visible=False)

# Criando o aplicativo Flask
app = Flask(__name__)

# Rota para renderizar o template com o gráfico
@app.route('/')
def renderizar_grafico():
    return render_template('grafico_candles.html', acao=acao, plot=figura.to_html())

if __name__ == '__main__':
    app.run(debug=True)
