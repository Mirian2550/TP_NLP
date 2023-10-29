"""
import pandas as pd
import nltk
import spacy
from nltk.corpus import stopwords

nltk.download('stopwords')
spacy.cli.download("es_core_news_sm")
nlp = spacy.load("es_core_news_sm")
nlp.max_length = 3000000


def summarize_category(category, word_count=100):
    data = pd.read_csv('../data/dataset.csv', delimiter='|')
    data_filtrado = data[data['category'] == category]
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

import pandas as pd
import spacy
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
spacy.cli.download("es_core_news_sm")
nlp = spacy.load("es_core_news_sm")
nlp.max_length = 3000000

def summarize_category( category, word_count=100):
    """
    Summarize news articles from a specific category.

    Parameters:
    - category (str): The category to filter the news articles.
    - word_count (int): Maximum word count for each summary fragment.

    Returns:
    - Generator: A generator that yields summary fragments.
    """
    # Load news data from CSV
    data = pd.read_csv('../data/dataset.csv', delimiter='|')

    # Filter news articles by category
    data_filtrado = data[data['category'] == category]

    # Combine text from filtered articles
    text = ' '.join(data_filtrado['text'].astype(str))

    # Tokenize and lemmatize the text
    doc = nlp(text)

    # Get Spanish stopwords
    stop_words = set(stopwords.words('spanish'))

    # Lemmatize words and remove stopwords
    lemmatized_words = [token.lemma_ for token in doc if token.text.lower() not in stop_words]

    # Join lemmatized words
    text_to_summarize = ' '.join(lemmatized_words)

    # Split the text into fragments
    start = 0
    while start < len(text_to_summarize):
        end = start + word_count
        if end > len(text_to_summarize):
            end = len(text_to_summarize)

        yield text_to_summarize[start:end]

        start = end




