# -*- coding: utf-8 -*-
"""
This Example will show you how to use register_next_step handler.
"""

import telebot
from telebot import types


TOKEN = '703378718:AAEmJpyicXr2Ym6HGttJhgPWIGlCrGZtQOc'
bot = telebot.TeleBot(TOKEN)

user_dict = {}


class User:
    def __init__(self, km):
        self.km = km
        self.rashod = None
        self.price = None

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id,'''
    Welcome! Это простой бот для расчета стоимости поездки на автомобиле.
    При выборе команды /fuel бот задаст вам несколько вопросов и расчитает стоимость поездки.
    ''')

# Handle '/start' and '/help'
@bot.message_handler(commands=['fuel'])
def send_question(message):
    msg = bot.reply_to(message, """\
Введите количество пройденных киломметров: 
""")
    bot.register_next_step_handler(msg, process_km_step)


def is_float(s):
    try:
        float(s)
        return True
    except ValueError: 
        return False

def process_km_step(message):
    try:
        chat_id = message.chat.id
        km = message.text
        if not km.isdigit():
            msg = bot.reply_to(message, 'Только целые числа пожалуйста! ')
            bot.register_next_step_handler(msg, process_km_step)
            return

        user = User(km)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Отлично! Теперь введите расход вашего автомобиля:')
        bot.register_next_step_handler(msg, process_rashod_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_rashod_step(message):
    try:
        chat_id = message.chat.id
        rashod = message.text
        if not rashod.isdigit():
            msg = bot.reply_to(message, 'Только числа пожалуйста!')
            bot.register_next_step_handler(msg, process_rashod_step)
            return
        user = user_dict[chat_id]
        user.rashod = rashod
    #    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
     #   markup.add('Male', 'Female')
        msg = bot.reply_to(message, 'И последний вопрос! Какая стоимость одного литра бензина?')
        bot.register_next_step_handler(msg, process_price_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_price_step(message):
    try:
        chat_id = message.chat.id
        price = message.text
        if is_float(price) == False:
            msg = bot.reply_to(message, 'Только числа пожалуйста! ')
            bot.register_next_step_handler(msg, process_price_step)
            return

        user = user_dict[chat_id]
#        if (sex == u'Male') or (sex == u'Female'):
        user.price = price
        #else:
            #raise Exception()

        V = (int(user.rashod) * int(user.km)) / 100

        SUMMA = V * float(user.price)

        bot.send_message(chat_id, 'Стоимость вашей поездки составила: ' + str(SUMMA))
    except Exception as e:
        bot.reply_to(message, 'oooops')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()