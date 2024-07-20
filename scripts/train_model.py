import spacy
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline

# Datos de entrenamiento
data = [
    ("busca información de Python", "Python"),
    ("busca Java", "Java"),
    ("busca sobre Inteligencia Artificial", "Inteligencia Artificial"),
    ("dime algo sobre Machine Learning", "Machine Learning"),
    ("busca información de modelos de lenguaje", "modelos de lenguaje"),
    ("busca Python", "Python"),
    ("busca sobre aprendizaje profundo", "aprendizaje profundo"),
    ("dime algo sobre redes neuronales", "redes neuronales"),
]

# Separar datos y etiquetas
texts, labels = zip(*data)

# Cargar el modelo de lenguaje de spaCy
nlp = spacy.load("en_core_web_sm")

# Preprocesamiento: Extraer características (tokens) de las oraciones
def preprocess(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

# Preprocesar los textos
preprocessed_texts = [preprocess(text) for text in texts]

# Vectorización y Modelo
vectorizer = CountVectorizer()
classifier = RandomForestClassifier()

# Crear pipeline de procesamiento y clasificación
model = make_pipeline(vectorizer, classifier)

# Entrenar el modelo
model.fit(preprocessed_texts, labels)

# Función para predecir la palabra clave
def predict_keyword(phrase):
    preprocessed_phrase = preprocess(phrase)
    return model.predict([preprocessed_phrase])[0]

# Prueba del modelo
test_phrases = [
    "busca información de Data Science",
    "busca C++",
    "busca sobre Deep Learning",
    "dime algo sobre Natural Language Processing",
]

for phrase in test_phrases:
    print(f"Frase: {phrase} -> Palabra clave: {predict_keyword(phrase)}")
