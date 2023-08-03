import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ta.momentum import RSIIndicator
from flask import Flask, render_template, request
from datetime import datetime

# Criando o aplicativo Flask
app = Flask(__name__)

# Função para criar o gráfico com os dados da ação
def criar_grafico_acao(acao):
    start = '2018-06-01'
    end = datetime.today()
    
    # Obtendo os dados históricos da ação
    dados_acao = yf.download(acao, start=start, end=end)

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
                                 name=acao,
                                 increasing_line_color='blue',  # Cor das candles de alta
                                 decreasing_line_color='red'    # Cor das candles de baixa
    )

    # Criando o gráfico de barras para o volume
    volume = go.Bar(x=dados_acao.index,
                    y=dados_acao['Volume'],
                    name='Volume')

    # Criando as linhas para as médias móveis
    ma9 = go.Scatter(x=dados_acao.index, 
                     y=dados_acao['MA9'],
                     line=dict(color='green', width=1.5),  # Cor da MA9
                     name='MA9')

    ma21 = go.Scatter(x=dados_acao.index,
                      y=dados_acao['MA21'],
                      line=dict(color='orange', width=1.5), # Cor da MA21
                      name='MA21')

    # Criando o gráfico de linha para o RSI
    rsi = go.Scatter(x=dados_acao.index, 
                     y=dados_acao['RSI'], 
                     line=dict(color='purple', width=1.5),  # Cor do RSI
                     name='RSI')

    # Criando a figura com os gráficos de candles, volume, médias móveis e RSI
    figura = make_subplots(rows=3, 
                           cols=1, 
                           shared_xaxes=True, 
                           vertical_spacing=0.05,
                           row_heights=[0.6, 0.2, 0.2],
                           #subplot_titles=("Gráfico de Candles", "Volume", "Médias Móveis", "RSI")
                           )

    figura.add_trace(candlestick, row=1, col=1)
    figura.add_trace(volume, row=2, col=1)
    figura.add_trace(ma9, row=1, col=1)
    figura.add_trace(ma21, row=1, col=1)
    figura.add_trace(rsi, row=3, col=1)

    # Atualizando o layout do gráfico
    figura.update_layout(title=f'Gráfico de Candles, Volume, Médias Móveis e RSI da Ação {acao}',
                         #xaxis_title='Data',
                         xaxis_rangeslider_visible=False,
                         width=1000, 
                         height=800, 
                         font=dict(family='Arial', size=12),  
                         paper_bgcolor='rgba(0,0,0,0)',  
                         plot_bgcolor='rgba(0,0,0,0)',   
                         hovermode='x unified',  
                         legend=dict(font=dict(family='Arial', size=12),  
                                     bgcolor='rgba(0,0,0,0)'),
                         
                         xaxis=dict(showgrid=True, 
                                    gridcolor='lightgray'),  # Adicionar grid no eixo x
                         
                         yaxis=dict(showgrid=True, 
                                    gridcolor='lightgray'),  # Adicionar grid no eixo y
                         
                         margin=dict(l=50, r=50, t=80, b=50)  # Ajustar as margens do gráfico
    )

    return figura

# Rota principal para renderizar o template com o gráfico
@app.route('/', methods=['GET', 'POST'])
def renderizar_grafico():
    acao = 'AAPL'  # Ação padrão
    if request.method == 'POST':
        # Verificar se o usuário enviou uma ação para análise
        if 'acao' in request.form:
            acao = request.form['acao']
    
    # Criar o gráfico da ação escolhida
    figura = criar_grafico_acao(acao)

    # Mostrar a figura atualizada
    plot_html = figura.to_html()

    return render_template('grafico_candles.html', 
                           acao=acao, 
                           plot=plot_html)

# Executar o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)
    