import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ta.momentum import RSIIndicator
from flask import Flask, render_template, request

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
                       subplot_titles=("Gráfico de Candles", "Volume", "Médias Móveis", "RSI"))

figura.add_trace(candlestick, row=1, col=1)
figura.add_trace(volume, row=2, col=1)
figura.add_trace(ma9, row=1, col=1)
figura.add_trace(ma21, row=1, col=1)
figura.add_trace(rsi, row=3, col=1)

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
                     ),
                     xaxis=dict(showgrid=True, gridcolor='lightgray'),  # Adicionar grid no eixo x
                     yaxis=dict(showgrid=True, gridcolor='lightgray'),  # Adicionar grid no eixo y
                     margin=dict(l=50, r=50, t=80, b=50)  # Ajustar as margens do gráfico
)

# Criando o aplicativo Flask
app = Flask(__name__)

# Rota para renderizar o template com o gráfico
@app.route('/', methods=['GET', 'POST'])
def renderizar_grafico():
    linha = None
    if request.method == 'POST':
        # Verificar se o usuário enviou um valor para a linha
        if 'linha' in request.form:
            linha = float(request.form['linha'])
    
    # Criar uma nova figura para evitar conflito com gráficos anteriores
    nova_figura = figura.copy()

    # Adicionar a linha no gráfico de candles, se o valor estiver definido
    if linha is not None:
        linha_horizontal = go.Scatter(x=dados_acao.index,
                                      y=[linha] * len(dados_acao),
                                      line=dict(color='red', dash='dash'),
                                      name='Linha')
        nova_figura.add_trace(linha_horizontal, row=1, col=1)

    # Mostrar a figura atualizada
    plot_html = nova_figura.to_html()

    return render_template('grafico_candles.html', acao=acao, plot=plot_html)

# Executar o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)
