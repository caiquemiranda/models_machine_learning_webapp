import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from flask import Flask, render_template

# Obtendo os dados históricos da ação do Facebook
acao_facebook = yf.download('FB', start='2022-01-01', end='2023-01-01')

# Criando o aplicativo Flask
app = Flask(__name__)

# Rota para renderizar o gráfico de candles da ação do Facebook
@app.route('/')
def plot_candlestick():
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    # Gráfico de candles
    fig.add_trace(go.Candlestick(x=acao_facebook.index,
                                 open=acao_facebook['Open'],
                                 high=acao_facebook['High'],
                                 low=acao_facebook['Low'],
                                 close=acao_facebook['Close'],
                                 name='FB'), row=1, col=1)

    # Gráfico de volume
    fig.add_trace(go.Bar(x=acao_facebook.index,
                         y=acao_facebook['Volume'],
                         name='Volume'), row=2, col=1)

    fig.update_layout(title='Gráfico de Candles e Volume da Ação do Facebook (FB)',
                      xaxis_title='Data',
                      yaxis_title='Preço',
                      yaxis2_title='Volume',
                      showlegend=False)

    return render_template('candlestick_plot.html', plot=fig.to_html())

if __name__ == '__main__':
    app.run(debug=True)
