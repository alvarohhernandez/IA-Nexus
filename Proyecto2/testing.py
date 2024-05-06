import joblib
import argparse
import pandas as pd
from utils import preprocess_text

# Importar el módulo argparse para manejar los argumentos de línea de comandos
parser = argparse.ArgumentParser(description='Procesamiento de datos de texto y clasificación con Random Forest.')
parser.add_argument('csv_file', type=str, help='Ruta al archivo CSV que contiene los datos de entrada')

# Parsear los argumentos de línea de comandos
args = parser.parse_args()

# Cargar el modelo entrenado y otros objetos necesarios
model = joblib.load('modelo_random_forest.pkl')
vectorizer = joblib.load('vectorizador_tfidf.pkl')
label_encoder = joblib.load('codificador_etiquetas.pkl')

# Cargar el archivo CSV con las frases a clasificar
df_test = pd.read_csv(args.csv_file, names=['text'], header=None)

# Preprocesamiento de texto
texts = df_test['text'].apply(preprocess_text)

# Representación de texto
X_test = vectorizer.transform(texts)

# Clasificación
y_pred = model.predict(X_test)

# Decodificar las etiquetas predichas
predicted_labels = label_encoder.inverse_transform(y_pred)

# Agregar las etiquetas predichas al DataFrame
df_test['categoria'] = predicted_labels

# Guardar los resultados en un nuevo archivo CSV
df_test.to_csv('resultados_prediccion.csv', index=False)
