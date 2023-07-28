import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ta.momentum import RSIIndicator
from flask import Flask, render_template

# Ação para análise
acao = 'AAPL'  # Altere para a ação desejada

# Obtendo os dados históricos da ação
dados_acao = yf.download(acao, start='2023-01-01', end='2023-06-01')

# Calculando as médias móveis de 9 e 21 períodos
dados_acao['MA9'] = dados_acao['Close'].rolling(window=9).mean()
dados_acao['MA21'] = dados_acao['Close'].rolling(window=21).mean()

# Calculando o RSI com um período de 14
rsi_indicator = RSIIndicator(dados_acao['Close'], window=14)
dados_acao['RSI'] = rsi_indicator.rsi()

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

# Criando as linhas para as médias móveis
ma9 = go.Scatter(x=dados_acao.index, 
                 y=dados_acao['MA9'],
                 line=dict(color='blue', width=0.75),
                 name='MA9')

ma21 = go.Scatter(x=dados_acao.index,
                  y=dados_acao['MA21'],
                  line=dict(color='orange', 
                            width=1.5), 
                  name='MA21')

# Criando o gráfico de linha para o RSI
rsi = go.Scatter(x=dados_acao.index, 
                 y=dados_acao['RSI'], 
                 line=dict(color='green', width=1.5),
                 name='RSI')

# Criando a figura com os gráficos de candles, volume, médias móveis e RSI
figura = make_subplots(rows=3, 
                       cols=1, 
                       shared_xaxes=True, 
                       vertical_spacing=0.05,
                       row_heights=[0.7, 0.15, 0.15],
                       subplot_titles=("Gráfico de Candles", "Volume", "Médias Móveis", "RSI"))

figura.add_trace(candlestick, row=1, col=1)
#figura.add_trace(volume, row=2, col=1)
figura.add_trace(ma9, row=1, col=1)
figura.add_trace(ma21, row=1, col=1)
#figura.add_trace(rsi, row=3, col=1)

# Atualizando o layout do gráfico
figura.update_layout(title=f'Gráfico de Candles, Volume, Médias Móveis e RSI da Ação {acao}',
                     xaxis_title='Data',
                     xaxis_rangeslider_visible=False)

# Personalizando as cores das linhas e candles
candlestick = go.Candlestick(x=dados_acao.index,
                             open=dados_acao['Open'],
                             high=dados_acao['High'],
                             low=dados_acao['Low'],
                             close=dados_acao['Close'],
                             name=acao,
                             increasing_line_color='blue',  # Cor das candles de alta
                             decreasing_line_color='red'    # Cor das candles de baixa
)

# Personalizando as cores das médias móveis e RSI
ma9 = go.Scatter(x=dados_acao.index, 
                 y=dados_acao['MA9'],
                 line=dict(color='green', width=1.5),  # Cor da MA9
                 name='MA9')

ma21 = go.Scatter(x=dados_acao.index,
                  y=dados_acao['MA21'],
                  line=dict(color='orange', width=1.5), # Cor da MA21
                  name='MA21')

rsi = go.Scatter(x=dados_acao.index, 
                 y=dados_acao['RSI'], 
                 line=dict(color='purple', width=1.5),  # Cor do RSI
                 name='RSI')

# Atualizando o layout do gráfico
figura.update_layout(title=f'Gráfico de Candles, Volume, Médias Móveis e RSI da Ação {acao}',
                     xaxis_title='Data',
                     xaxis_rangeslider_visible=False,
                     width=1000,  # Ajuste a largura da figura (aumente ou diminua conforme necessário)
                     height=800,  # Ajuste a altura da figura (aumente ou diminua conforme necessário)
                     font=dict(family='Arial', size=12),  # Estilo de fonte dos textos do gráfico
                     paper_bgcolor='rgba(0,0,0,0)',  # Fundo transparente
                     plot_bgcolor='rgba(0,0,0,0)',   # Fundo transparente
                     hovermode='x unified',  # Mostrar dicas de ferramentas de forma unificada
                     legend=dict(font=dict(family='Arial', size=12),  # Estilo de fonte da legenda
                                 bgcolor='rgba(0,0,0,0)'  # Fundo transparente para a legenda
                     )
)

# Criando o aplicativo Flask
app = Flask(__name__)

# Rota para renderizar o template com o gráfico
@app.route('/')
def renderizar_grafico():
    return render_template('grafico_candles.html', acao=acao, plot=figura.to_html())

if __name__ == '__main__':
    app.run(debug=True)
