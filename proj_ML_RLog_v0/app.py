from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Carregando o modelo treinado
modelo_salvo = joblib.load('modelo_regressao_logistica.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        valor_caracteristica = float(request.form['caracteristica'])
    except ValueError:
        return render_template('index.html', mensagem="Valor inválido. Insira um número válido.")

    dados_usuario = np.array([[valor_caracteristica]])
    previsao_usuario = modelo_salvo.predict(dados_usuario)
    previsao_texto = 'Classe 0' if previsao_usuario[0] == 0 else 'Classe 1'
    return render_template('index.html', previsao=previsao_texto)

if __name__ == '__main__':
    app.run(debug=True)
