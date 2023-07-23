import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

# Função para treinar o modelo de regressão logística
def treinar_modelo(X, y):
    modelo = LogisticRegression()
    modelo.fit(X, y)
    return modelo

# Função para avaliar o desempenho do modelo
def avaliar_modelo(modelo, X_test, y_test):
    previsoes = modelo.predict(X_test)
    acuracia = accuracy_score(y_test, previsoes)
    matriz_confusao = confusion_matrix(y_test, previsoes)
    return acuracia, matriz_confusao

# Dados de exemplo para treinamento
X = np.array([[2], [3], [5], [7], [10]])
y = np.array([0, 0, 1, 1, 1])

# Dividindo os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinando o modelo
modelo = treinar_modelo(X_train, y_train)

# Avaliando o desempenho do modelo
acuracia, matriz_confusao = avaliar_modelo(modelo, X_test, y_test)

print("Acurácia do modelo:", acuracia)
print("Matriz de Confusão:")
print(matriz_confusao)

# Visualizando a fronteira de decisão do modelo
x_min, x_max = X.min() - 1, X.max() + 1
x_range = np.linspace(x_min, x_max, 1000)
y_prob = modelo.predict_proba(x_range.reshape(-1, 1))[:, 1]

plt.scatter(X_train, y_train, color='blue', label='Dados de treinamento')
plt.scatter(X_test, y_test, color='red', label='Dados de teste')
plt.plot(x_range, y_prob, color='green', label='Fronteira de decisão')
plt.xlabel('Características')
plt.ylabel('Rótulos')
plt.legend()
plt.show()

# Salvando o modelo treinado em um arquivo
joblib.dump(modelo, 'modelo_regressao_logistica.joblib')

# Carregando o modelo treinado de volta a partir do arquivo
modelo_salvo = joblib.load('modelo_regressao_logistica.joblib')

# Loop para permitir que o usuário faça várias previsões
while True:
    dados_usuario = input("Insira o valor da característica (ou digite 'sair' para encerrar): ")
    if dados_usuario.lower() == 'sair':
        break
    try:
        valor_caracteristica = float(dados_usuario)
    except ValueError:
        print("Valor inválido. Insira um número válido.")
        continue

    dados_usuario = np.array([[valor_caracteristica]])
    previsao_usuario = modelo_salvo.predict(dados_usuario)
    print("Previsão para o valor da característica", valor_caracteristica, ":", previsao_usuario[0])

print("Obrigado por usar o modelo de regressão logística!")
