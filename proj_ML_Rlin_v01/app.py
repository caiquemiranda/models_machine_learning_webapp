from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Carregar o modelo treinado
modelo_carregado = joblib.load("modelo_regressao_linear.joblib")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prever', methods=['POST'])
def prever():
    try:
        entrada = float(request.form['entrada'])
        previsao = modelo_carregado.predict(np.array([entrada]).reshape(-1, 1))
        return render_template('resultado.html', entrada=entrada, previsao=previsao[0])
    except ValueError:
        return render_template('erro.html')

if __name__ == '__main__':
    app.run(debug=True)
