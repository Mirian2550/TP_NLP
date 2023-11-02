import telebot
from telebot import types
import logging
import spacy
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from transformers import BartTokenizer, BertModel
import torch
from transformers import BartForConditionalGeneration, BartTokenizer

def resumir_texto_bart(texto, max_caracteres=800):
    model_name = "facebook/bart-large-cnn"
    model = BartForConditionalGeneration.from_pretrained(model_name)
    tokenizer = BartTokenizer.from_pretrained(model_name)
    inputs = tokenizer(texto, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=max_caracteres, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def summary_test(categoria):
    data = pd.read_csv('C:/Users/Usuario/Documents/4TO CUATRIMESTRE/Procesamiento del lenguaje natural/Trabajo_Practico1/TP_NLP/data/dataset.csv', delimiter='|')
    data_filtrado = data[data['category'] == categoria]
    columna_texto = data_filtrado['text']
    all_news = '\n'.join(columna_texto.astype(str))
    summaries = list(resumir_texto_bart(all_news, max_caracteres=3000).split("\n"))
    return summaries


# Inicializa el bot de Telegram con tu token
bot = telebot.TeleBot('6430745292:AAG8DIz-jbjG9qdPJNA7MqZSiG0qy71W05w')



# Maneja el comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Bienvenido a mi bot de noticias! Ingresa /categorias para ver las categorías disponibles.")

# Maneja el comando /categorias
@bot.message_handler(commands=['categorias'])
def send_categories(message):
    # Puedes personalizar las categorías disponibles aquí
    keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    categories = ['Deportes', 'Recetas', 'Seguridad Informatica', 'Bebes']  # Personaliza con tus categorías
    for category in categories:
        keyboard.add(category)
    bot.send_message(message.chat.id, "Elige una categoría:", reply_markup=keyboard)

# Maneja las respuestas del usuario a las categorías
@bot.message_handler(func=lambda message: True)
def handle_category(message):
    category = message.text
    summaries = list(summary_test(category))
    
    if len(summaries) == 0:
        bot.send_message(message.chat.id, "No hay noticias disponibles para esta categoría.")
    else:
        for summary in summaries:
            bot.send_message(message.chat.id, summary)

# Inicia el bot
bot.polling()

"""
TOKEN = '6430745292:AAG8DIz-jbjG9qdPJNA7MqZSiG0qy71W05w'
MAX_SUMMARY_FRAGMENTS = 8
logging.basicConfig(filename='bot.log', level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)

nlp = spacy.load('es_core_news_sm')


def create_category_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item_recetas = types.KeyboardButton('Recetas')
    item_deportes = types.KeyboardButton('Deportes')
    item_tecnologia = types.KeyboardButton('Tecnología')
    item_seguridad_informatica = types.KeyboardButton('Seguridad Informatica')
    item_reiniciar = types.KeyboardButton('Reiniciar Bot')
    markup.row(item_recetas, item_deportes)
    markup.row(item_tecnologia, item_seguridad_informatica)
    markup.row(item_reiniciar)
    return markup


def start_bot():
    try:
        bot.polling()
    except Exception as e:
        logger.error("Error en start_bot: %s", str(e))
        start_bot()  # Reiniciar el bot en caso de un error


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        bot.send_message(message.chat.id, "¡Hola! Soy un bot de resumen. ¡Bienvenido!",
                         reply_markup=create_category_keyboard())
    except Exception as e:
        logger.error("Error en handle_start: %s", str(e))
        start_bot()  # Reiniciar el bot en caso de un error


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        if message.text == 'Recetas':
            bot.reply_to(message, "¡Has seleccionado la categoría de Recetas!")
            category_summary_generator = summarize_category('recetas')
            initial_summary = next(category_summary_generator)  # Realizar una carga inicial
            bot.send_message(message.chat.id, initial_summary)
            for i in range(MAX_SUMMARY_FRAGMENTS):
                partial_summary = next(category_summary_generator, None)
                if partial_summary is not None:
                    bot.send_message(message.chat.id, partial_summary)
                else:
                    break
        elif message.text == 'Deportes':
            bot.reply_to(message, "¡Has seleccionado la categoría de Deportes!")
            category_summary_generator = summarize_category('deportes')
            initial_summary = next(category_summary_generator)  # Realizar una carga inicial
            bot.send_message(message.chat.id, initial_summary)
            for i in range(MAX_SUMMARY_FRAGMENTS):
                partial_summary = next(category_summary_generator, None)
                if partial_summary is not None:
                    bot.send_message(message.chat.id, partial_summary)
                else:
                    break
        elif message.text == 'Tecnología':
            bot.reply_to(message, "¡Has seleccionado la categoría de Tecnología!")
            category_summary_generator = summarize_category('tecnologia')
            initial_summary = next(category_summary_generator)  # Realizar una carga inicial
            bot.send_message(message.chat.id, initial_summary)
            for i in range(MAX_SUMMARY_FRAGMENTS):
                partial_summary = next(category_summary_generator, None)
                if partial_summary is not None:
                    bot.send_message(message.chat.id, partial_summary)
                else:
                    break
        elif message.text == 'Seguridad Informatica':
            bot.reply_to(message, "¡Has seleccionado la categoría de Seguridad Informática!")
            category_summary_generator = summarize_category('Seguridad Informatica')
            initial_summary = next(category_summary_generator)  # Realizar una carga inicial
            bot.send_message(message.chat.id, initial_summary)
            for i in range(MAX_SUMMARY_FRAGMENTS):
                partial_summary = next(category_summary_generator, None)
                if partial_summary is not None:
                    bot.send_message(message.chat.id, partial_summary)
                else:
                    break
        elif message.text == 'Reiniciar Bot':
            bot.reply_to(message, "Bot reiniciado. Selecciona una categoría del teclado.",
                         reply_markup=create_category_keyboard())
        else:
            bot.reply_to(message, "Lo siento, no entiendo ese comando. Selecciona una categoría del teclado.")
    except Exception as e:
        logger.error("Error en handle_text: %s", str(e))
        start_bot()  # Reiniciar el bot en caso de un error


@bot.message_handler(commands=['info'])
def handle_info(message):
    try:
        info_message = "Comandos habilitados:\n\n"
        info_message += "/start - Iniciar el bot y ver las categorías\n"
        info_message += "/info - Mostrar información sobre los comandos habilitados\n"
        info_message += "Categorías:\n"
        info_message += " - Recetas\n"
        info_message += " - Deportes\n"
        info_message += " - Tecnología\n"
        info_message += " - Seguridad Informática\n"
        info_message += " - Reiniciar Bot"
        bot.send_message(message.chat.id, info_message)
    except Exception as e:
        logger.error("Error en handle_info: %s", str(e))
        start_bot()


start_bot()
"""