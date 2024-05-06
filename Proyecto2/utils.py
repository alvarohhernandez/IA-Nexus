import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('spanish'))

# Función para preprocesar texto
def preprocess_text(text):
    # Realizamos Tokenización
    corpus = word_tokenize(text.lower())
    # Eliminamos stopwords
    corpus = [word for word in corpus if word not in stop_words]
    # Realizamos lematización
    corpus = [lemmatizer.lemmatize(word) for word in corpus]
    # Eliminamos caracteres especiales y puntuación
    corpus = [word for word in corpus if word not in string.punctuation]
    # Eliminamos corpus vacíos en caso de existir
    corpus = [word for word in corpus if word.strip()]
    # Convertimos corpus nuevamente a texto
    return ' '.join(corpus)
