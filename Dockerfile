FROM python:3.10
WORKDIR /app
COPY TelegramBot/ /app
COPY requirements_bot.txt /app/requirements.txt
RUN pip install -r requirements.txt
CMD [ "python", "bot.py" ]