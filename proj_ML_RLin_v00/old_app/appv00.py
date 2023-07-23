import numpy as np
from flask import Flask, request, render_template

# Gerar dados aleatórios para X e y
np.random.seed(42)
X = np.random.rand(50, 1)
y = 2 + 3 * X + np.random.randn(50, 1)

# Dividir os dados em conjuntos de treinamento e teste (não é necessário no web app)
# Apenas para fins de ilustração, pois não utilizaremos o modelo treinado aqui
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar o objeto do modelo de regressão linear (não é necessário no web app)
# Apenas para fins de ilustração, pois não utilizaremos o modelo treinado aqui
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)

# Criar o aplicativo Flask
app = Flask(__name__)

# Rota para renderizar a página inicial com o layout moderno
@app.route('/')
def index():
    return render_template('index.html')

# Rota para lidar com a requisição do formulário e fazer a previsão
@app.route('/prever', methods=['GET'])
def prever():
    try:
        valor_X = float(request.args.get('X'))
        previsao = fazer_previsao(valor_X)
        return str(previsao)
    except ValueError:
        return "Erro: Insira um valor numérico válido para X."

# Função para fazer previsões usando o modelo treinado (não é necessário no web app)
# Apenas para fins de ilustração, pois não utilizaremos o modelo treinado aqui
def fazer_previsao(valor_X):
    return model.predict([[valor_X]])[0][0]

if __name__ == '__main__':
    app.run(debug=True)
