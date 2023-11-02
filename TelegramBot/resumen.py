import pandas as pd
import nltk
import spacy
from nltk.corpus import stopwords

nltk.download('stopwords')
spacy.cli.download("es_core_news_sm")
nlp = spacy.load("es_core_news_sm")
nlp.max_length = 3000000

def summarize_category(category, word_count=100):
    data = pd.read_csv('C:/Users/Usuario/Documents/4TO CUATRIMESTRE/Procesamiento del lenguaje natural/Trabajo_Practico1/TP_NLP/data/dataset.csv', delimiter='|')
    
    data_filtrado = data[data['category'] == category]
    
    if data_filtrado.empty:
        return "No hay noticias en esta categoría."
    
    text_category = ''
    
    for index, row in data_filtrado.iterrows():
        text_value = str(row['text'])  # Convierte el valor a cadena
        text_category += text_value.lower() + ' '
    
    doc = nlp(text_category)
    
    stop_words = set(stopwords.words('spanish'))
    
    lemmatized_words = [token.lemma_ for token in doc if token.text.lower() not in stop_words]
    text_to_summarize = ' '.join(lemmatized_words)

    start = 0
    while start < len(text_to_summarize):
        end = start + word_count
        if end > len(text_to_summarize):
            end = len(text_to_summarize)

        yield text_to_summarize[start:end]

        start = end
"""



def summarize_category(category, word_count=100):
    data = pd.read_csv('C:/Users/Usuario/Documents/4TO CUATRIMESTRE/Procesamiento del lenguaje natural/Trabajo_Practico1/TP_NLP/data/dataset.csv', delimiter='|')
    data_filtrado = data[data['category;'] == category]
    data_filtrado.loc[:, 'text'] = data_filtrado['text'].astype(str)
    text = data_filtrado['text']
    text_category = ' '.join(text).lower()
    doc = nlp(text_category)
    stop_words = set(stopwords.words('spanish'))
    lemmatized_words = [token.lemma_ for token in doc if token.text.lower() not in stop_words]
    text_to_summarize = ' '.join(lemmatized_words)

    start = 0
    while start < len(text_to_summarize):
        end = start + word_count
        if end > len(text_to_summarize):
            end = len(text_to_summarize)

        yield text_to_summarize[start:end]

        start = end
"""


