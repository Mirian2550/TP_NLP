import logging
import pandas as pd
import telebot
from telebot import types
from transformers import BartForConditionalGeneration, BartTokenizer

TOKEN = '6977913405:AAFRzBHG-tmH5To5qw5iBOAwU-Qhafx0mng'
bot = telebot.TeleBot(TOKEN)
logging.basicConfig(filename='bot.log', level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)


def resumir_texto_bart(texto, max_caracteres=800, model=model, tokenizer=tokenizer):
    inputs = tokenizer(texto, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=max_caracteres, min_length=50, length_penalty=2.0,
                                 num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


def summarize_category(categoria):
    data = pd.read_csv('dataset.csv', delimiter='|')
    data_filtrado = data[data['category'] == categoria]
    columna_texto = data_filtrado['text']
    all_news = '\n'.join(columna_texto.astype(str))
    all_news = all_news.replace('and','y')
    all_news = all_news.replace('with', 'con')
    all_news = all_news.replace('the', 'el')
    all_news = all_news.replace('that', '')

    summaries = list(resumir_texto_bart(all_news, max_caracteres=3000).split("\n"))
    return summaries


conversacion_reiniciada = False


def create_category_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    security_button = types.KeyboardButton("Seguridad Informática")
    recipes_button = types.KeyboardButton("Recetas")
    babies_button = types.KeyboardButton("Bebés")
    sports_button = types.KeyboardButton("Deporte")
    restart_button = types.KeyboardButton("Reiniciar")
    keyboard.row(security_button, recipes_button)
    keyboard.row(babies_button, sports_button)
    keyboard.row(restart_button)
    keyboard.one_time_keyboard = True
    keyboard.remove_keyboard = True
    return keyboard


@bot.message_handler(func=lambda message: message.text == "Reiniciar")
def handle_restart(message):
    bot.send_message(message.chat.id, "La conversación ha sido reiniciada.",
                     reply_markup=create_category_keyboard())


@bot.message_handler(func=lambda message: message.text == "Seguridad Informática")
def handle_security(message):
    result = summarize_category('Seguridad Informatica')
    bot.send_message(message.chat.id, result)


@bot.message_handler(func=lambda message: message.text == "Recetas")
def handle_recipes(message):
    result = summarize_category('Recetas')
    bot.send_message(message.chat.id, result)


@bot.message_handler(func=lambda message: message.text == "Bebés")
def handle_babies(message):
    result = summarize_category('Bebes')
    bot.send_message(message.chat.id, result)


@bot.message_handler(func=lambda message: message.text == "Deporte")
def handle_sports(message):
    result = summarize_category('Deportes')
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        bot.send_message(message.chat.id, "¡Hola! Soy un bot de resumen. ¡Bienvenido!",
                         reply_markup=create_category_keyboard())
    except Exception as e:
        logger.error("Error en handle_start: %s", str(e))


@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    if not conversacion_reiniciada:
        bot.reply_to(message, "Lo siento, solo puedes interactuar a través de los botones disponibles.")


if __name__ == '__main__':
    bot.polling()
