import yfinance as yf
import plotly.graph_objects as go
from flask import Flask, render_template

# Obtendo os dados históricos da ação do Facebook
acao_facebook = yf.download('FB', start='2022-01-01', end='2023-01-01')

# Criando o aplicativo Flask
app = Flask(__name__)

# Rota para renderizar o gráfico de candles da ação do Facebook
@app.route('/')
def plot_candlestick():
    fig = go.Figure(data=[go.Candlestick(x=acao_facebook.index,
                                        open=acao_facebook['Open'],
                                        high=acao_facebook['High'],
                                        low=acao_facebook['Low'],
                                        close=acao_facebook['Close'])])

    fig.update_layout(title='Gráfico de Candles da Ação do Facebook (FB)',
                      xaxis_title='Data',
                      yaxis_title='Preço',
                      yaxis2_title='Volume',
                      yaxis2=dict(overlaying='y', side='right'))

    return render_template('candlestick_plot.html', plot=fig.to_html())

if __name__ == '__main__':
    app.run(debug=True)