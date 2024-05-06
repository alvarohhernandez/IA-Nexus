import time
import joblib
import pandas as pd
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from utils import preprocess_text
from sklearn.metrics import f1_score
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from imblearn.under_sampling import RandomUnderSampler
from sklearn.feature_extraction.text import TfidfVectorizer


target_cols = ['clasismo','racismo','sexismo','otros','contenido_inapropiado','ninguna_de_las_anteriores']

# Carga y exploración de los datos
dfTexts = pd.read_csv('train_data.csv', names=['image', 'text'], header=None)

dfLabels = pd.read_table('train_labels_subtask_2.csv', delimiter=',', names=target_cols, header=None)

data_train = pd.concat([dfLabels, dfTexts], axis=1)

# Verificamos si el dataset está balanceado
class_counts = data_train.iloc[:, :-2].sum()
print(class_counts)

# Visualizamos la distribución de clases en una gráfica de barras
plt.figure(figsize=(8, 6))
class_counts.plot(kind='bar', color='skyblue')
plt.title('Distribución de memes por clase')
plt.xlabel('Clases')
plt.ylabel('Cantidad de memes')
plt.xticks(rotation=45)
plt.show()

# Cálculo de proporciones
total_memes = len(data_train)
class_proportions = class_counts / total_memes
print("Proporción de memes por clase:")
print(class_proportions)

# Dado que la clase "ninguna_de_las_anteriore" es significativamente
# más grande que las otras clases, podemos determinar que nuestro
# conjunto de datos está desbalanceado. Para abordar este problema
# usaremos SMOTE, una técnica para abordar el desbalance de clases al
# generar ejemplos sintéticos de la clase minoritaria.

# Ahora, realizamos el proceso de limpieza y preprocesamiento de datos
# antes de alimentarlos a un modelo de clasificación.

data_train['text'] = data_train['text'].apply(preprocess_text)

## Representación de Texto

# Convertimos los textos preprocesados en vectores numéricos que puedan
# ser entendidos por el modelo. Para ello utilizamos TF-IDF (Term
# Frequency-Inverse Document Frequency). ¿Por qué?
#
# TF-IDF es computacionalmente más eficiente para conjuntos de datos
# grandes.
# TF-IDF asigna pesos a las palabras en función de su importancia relativa
# en el documento y en el conjunto de documentos, lo que puede ser útil
# para resaltar términos importantes, que es precisamente lo que buscamos
# al categorizar memes inapropiados.

# Inicializamos el vectorizador TF-IDF
vectorizer = TfidfVectorizer()
# Aplicamos el vectorizador al texto preprocesado
X = vectorizer.fit_transform(data_train['text'])

# Aplicamos SMOTE para balancear las clases
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, data_train.iloc[:, :-2].idxmax(axis=1))

# 1. Conteo de muestras por clase
class_counts = pd.Series(y_resampled).value_counts()
print("Conteo de muestras por clase:")
print(class_counts)

# 2. Visualización
plt.figure(figsize=(8, 6))
class_counts.plot(kind='bar', color='skyblue')
plt.title('Distribución de clases después de SMOTE')
plt.xlabel('Clases')
plt.ylabel('Número de muestras')
plt.xticks(rotation=45)
plt.show()

# Selección del modelo
#
# Usaremos un diagrama de dispersión para tratar de elegir el modelo
# más adecuado. Un diagrama de dispersión proporciona información sobre
# la distribución de las clases en un espacio de menor dimesión generado
# por PCA. 

# Reducción de dimensionalidad con PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_resampled.toarray())

# Inicializar el codificador de etiquetas
label_encoder = LabelEncoder()

# Convertir los nombres de las clases a valores numéricos
y_resampled_encoded = label_encoder.fit_transform(y_resampled)

# Creamos un diagrama de dispersión para visualizar los datos en 2D
plt.figure(figsize=(10, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y_resampled_encoded, cmap='viridis')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.title('Diagrama de Dispersión con PCA')
plt.colorbar(label='Clase')
plt.show()

# Se selecciona Random Forest como módelo de clasificación:
# El diagrama de dispersión generado por PCA sugiere que las clases
# pueden no estar perfectamente serparadas por una frontera lineal.
# Random Forest es robusto ante datos no lineales, ya que construye
# múltiples árboles de decisión y combina sus resultados, lo que puede
# capturar relaciones no lineales entre las características y las clases.

# Random Fores maneja naturalmnete características irrelevantes o
# redundantes.

# Random Forest tiende a tener un buen rendimiento en conjuntos de datos
# grandes y complejos, y es menos propenso al sobreajute en comparación
# con modelos como los árboles de decisión individuales.

# Aunque hemos utilizado SMOTE para abordar el desbalance de clases,
# Random Forest tambien puede manejar conjuntos de datos desbalanceados
# de manera efectiva. Además, la combinación de múltiples árboles en
# Random Forest ayuda a reducir el impacto de las clase mayoritaria en
# la clasificació.

# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled_encoded, test_size=0.2, random_state=42)

# Definimos el modelo
random_forest = RandomForestClassifier(random_state=42)

# Entrenamos el modelo con el conjunto de entrenamiento
random_forest.fit(X_train, y_train)

# Función para evaluar un modelo y mostrar las métricas y la
# matriz de confusión.
def evaluar_modelo(modelo, X_test, y_test):
    # Predecir las etiquetas en el conjunto de prueba
    y_pred = modelo.predict(X_test)

    # Calcular métricas individuales
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average=None)
    recall = recall_score(y_test, y_pred, average=None)
    f1 = f1_score(y_test, y_pred, average=None)

    # Mostrar métricas individuales
    print("Accuracy:", accuracy)
    print("Precisión:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)

    # Mostrar métricas con classification_report
    print(classification_report(y_test, y_pred, target_names=target_cols))

    # Mostrar matriz de confusión
    matriz = confusion_matrix(y_test, y_pred)
    print("Matriz de Confusión:")
    print(matriz)

# Evaluamos el modelo Random Forest
print("Random Forest:")
evaluar_modelo(random_forest, X_test, y_test)

# Guardar el modelo entrenado
joblib.dump(random_forest, 'modelo_random_forest.pkl')

# Guardar el vectorizador TF-IDF
joblib.dump(vectorizer, 'vectorizador_tfidf.pkl')

# Guardar el codificador de etiquetas
joblib.dump(label_encoder, 'codificador_etiquetas.pkl')
