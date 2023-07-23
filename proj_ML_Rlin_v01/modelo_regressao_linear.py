# Importar as bibliotecas necessárias
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import joblib

# Dados de exemplo para treinamento do modelo (substitua estes dados pelos seus próprios dados)
X_treino = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
y_treino = np.array([2, 4, 5, 4, 5])

# Criar o modelo de regressão linear
modelo = LinearRegression()

# Treinar o modelo
modelo.fit(X_treino, y_treino)

# Fazer previsões com novos dados
X_novos_dados = np.array([6, 7, 8]).reshape(-1, 1)
predicoes_novos_dados = modelo.predict(X_novos_dados)

# Coeficientes da regressão
coeficiente_angular = modelo.coef_[0]
intercepto = modelo.intercept_

# Imprimir os resultados
print("Coeficiente Angular:", coeficiente_angular)
print("Intercepto:", intercepto)

# Avaliar o modelo - R-quadrado (R2)
r_squared = modelo.score(X_treino, y_treino)
print("R-quadrado (R2):", r_squared)

# Visualizar os resultados
plt.scatter(X_treino, y_treino, color='blue', label='Dados de treinamento')
plt.plot(X_treino, modelo.predict(X_treino), color='red', linewidth=2, label='Regressão Linear')
plt.scatter(X_novos_dados, predicoes_novos_dados, color='green', label='Novos dados - Previsões')
plt.xlabel('Variável Independente')
plt.ylabel('Variável Dependente')
plt.title('Regressão Linear')
plt.legend()
plt.show()

# Imprimir as previsões com os novos dados
print("Previsões com os novos dados:")
for i in range(len(X_novos_dados)):
    print(f"Entrada: {X_novos_dados[i][0]}, Previsão: {predicoes_novos_dados[i]}")

# Salvar o modelo treinado usando a biblioteca joblib
nome_arquivo_modelo = "modelo_regressao_linear.joblib"
joblib.dump(modelo, nome_arquivo_modelo)
print(f"Modelo treinado salvo em '{nome_arquivo_modelo}'")

# Carregar o modelo treinado
modelo_carregado = joblib.load(nome_arquivo_modelo)

# Fazer previsões usando o modelo carregado
predicoes_modelo_carregado = modelo_carregado.predict(X_novos_dados)

# Imprimir as previsões feitas pelo modelo carregado
print("Previsões com o modelo carregado:")
for i in range(len(X_novos_dados)):
    print(f"Entrada: {X_novos_dados[i][0]}, Previsão: {predicoes_modelo_carregado[i]}")
