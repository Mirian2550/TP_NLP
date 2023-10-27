import re
from nltk import word_tokenize
from nltk.corpus import stopwords
import pandas as pd

def resumen_categoria(categoria):
    data = pd.read_csv('data/dataset.csv')

    data_filtrado = data[data['category'] == categoria]

    columna_texto = data_filtrado['text']

    resumen = ' '.join(columna_texto.astype(str))

    return resumen

def procesar_texto(categoria):
    texto = resumen_categoria(categoria)
    
    texto = texto.lower()
    
    texto = re.sub(r'[^a-záéíóúüñ\s]', '', texto)
    
    palabras = word_tokenize(texto)
    
    stop_words = set(stopwords.words('spanish'))
    palabras = [palabra for palabra in palabras if palabra not in stop_words]
    
    return palabras