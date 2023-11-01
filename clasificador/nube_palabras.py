import multiprocessing

import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from .normalizador import procesar_texto

nltk.data.path.append('nltk_data')


def _nube_palabras(texto):
    palabras_procesadas, categoria = procesar_texto(texto)
    conteo_palabras = nltk.FreqDist(palabras_procesadas)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(
        conteo_palabras)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(categoria)
    plt.axis('off')
    plt.show()


def generar_nube_palabras():
    categorias = ['Seguridad Informatica', 'Bebes', 'Deportes', 'Recetas']
    processes = [multiprocessing.Process(target=_nube_palabras, args=(categoria,)) for categoria in categorias]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
