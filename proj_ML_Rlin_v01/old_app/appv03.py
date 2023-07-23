from flask import Flask, render_template, request
import numpy as np
import joblib
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Carregar o modelo treinado
modelo_carregado = joblib.load("modelo_regressao_linear.joblib")

def gerar_grafico(entrada, previsao):
    plt.figure(figsize=(8, 5))
    plt.scatter(entrada, previsao, color='blue', label='Previsão')
    plt.xlabel('Entrada')
    plt.ylabel('Previsão')
    plt.title('Resultado da Previsão')
    plt.legend()
    plt.grid(True)

    # Salvar o gráfico em um buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Codificar o gráfico em base64 para exibi-lo na página
    grafico_codificado = base64.b64encode(buffer.getvalue()).decode()

    return grafico_codificado

@app.route('/', methods=['GET', 'POST'])
def index():
    grafico = None
    previsao = None
    if request.method == 'POST':
        try:
            entrada = float(request.form['entrada'])
            previsao = modelo_carregado.predict(np.array([entrada]).reshape(-1, 1))[0]
            grafico = gerar_grafico(entrada, previsao)
        except ValueError:
            previsao = "Valor inválido"
    return render_template('index.html', previsao=previsao, grafico=grafico)

if __name__ == '__main__':
    app.run(debug=True)
