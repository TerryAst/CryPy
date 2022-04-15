from urllib.parse import urlencode
import telebot
from extensions import APIException, Convertor
from config import TOKEN, keys
import traceback


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Добро пожаловать в CryRy.\nЯ создан для помощи в расчете курса валют на текущий момент.\nНа данный момент я обучен командам:\n/start - приветствие и инструкция по работе CryPy\n/help - инструкция по работе\n/values - список доступных валют\nДля расчета стоимости валюты прошу ввести сообщение в формате <имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "/start - приветствие и инструкция по работе CryPy\n/help - инструкция по работе\n/values - список доступных валют\nДля расчета стоимости валюты прошу ввести сообщение в формате <имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in keys.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')
        
        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}" )
    else:
        bot.reply_to(message,answer)

bot.polling()