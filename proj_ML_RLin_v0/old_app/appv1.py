import numpy as np
from flask import Flask, request, render_template
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Gerar dados aleatórios para X e y
np.random.seed(42)
X = np.random.rand(50, 1)
y = 2 + 3 * X + np.random.randn(50, 1)

# Criar o aplicativo Flask
app = Flask(__name__)

# Rota para renderizar a página inicial com o layout moderno e o gráfico
@app.route('/')
def index():
    # Criar o gráfico de dispersão com os dados
    plt.figure(figsize=(8, 6))
    plt.scatter(X, y, label='Dados de exemplo', color='blue')
    
    # Ajustar o modelo de regressão linear aos dados (apenas para fins de ilustração)
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    plt.plot(X, y_pred, color='red', label='Regressão Linear')
    
    plt.xlabel('X')
    plt.ylabel('y')
    plt.legend()
    
    # Converter o gráfico para imagem e codificá-lo em base64 para ser exibido na página
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    
    plt.close()
    
    # Renderizar a página index.html com o gráfico codificado em base64
    return render_template('index.html', plot_data=plot_data)

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
    return 2 + 3 * valor_X

if __name__ == '__main__':
    app.run(debug=True)
