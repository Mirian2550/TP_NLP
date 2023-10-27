import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from .normalizador import procesar_texto


def generar_nube_palabras(texto):
    palabras_procesadas,categoria = procesar_texto(texto)

    conteo_palabras = nltk.FreqDist(palabras_procesadas)

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(conteo_palabras)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(categoria)
    plt.axis('off')
    plt.show()
