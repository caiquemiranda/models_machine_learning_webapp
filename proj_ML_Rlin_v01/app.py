from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Carregar o modelo treinado
modelo_carregado = joblib.load("modelo_regressao_linear.joblib")

@app.route('/', methods=['GET', 'POST'])
def index():
    previsao = None
    if request.method == 'POST':
        try:
            entrada = float(request.form['entrada'])
            previsao = modelo_carregado.predict(np.array([entrada]).reshape(-1, 1))[0]
        except ValueError:
            previsao = "Valor inválido"
    return render_template('index.html', previsao=previsao)

if __name__ == '__main__':
    app.run(debug=True)
