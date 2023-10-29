import telebot
from telebot import types
import logging
import spacy
from TelegramBot.resumen import summarize_category

TOKEN = '6464021236:AAH1nf0NepSAOAuh5nIJZJC36p-cxqAI7tw'
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
    item_seguridad_informatica = types.KeyboardButton('Seguridad Informática')
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
        elif message.text == 'Seguridad Informática':
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
