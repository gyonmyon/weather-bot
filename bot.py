# -*- coding: utf-8 -*-
import redis
import os
import telebot
#host from home
#import mytoken    

# import some_api_lib
# import ...
from pyowm import OWM
#Yobit function
from yobit import get_btc

# Example of your code beginning
#           Config vars
token = os.environ['TELEGRAM_TOKEN']
API_key = os.environ['API_key']
#             ...

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
# r = redis.from_url(os.environ.get("REDIS_URL"))

#       Your bot code below
# token-telegram
    #token = mytoken.TOKEN
bot = telebot.TeleBot(token)
# some_api = some_api_lib.connect(some_api_token)
#              ...
# OWM API

#host from home
    #API_key = mytoken.API_key

owm = OWM(API_key, language="ua")

@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
	pass

@bot.message_handler(regexp="\n\d{3}\d*")
def guess_city(message):
    '''Input number to guess a city
    '''
    obs = owm.weather_at_place(message.text)    
    l = obs.get_location()
    try:
        city_name = l.get_name()
        answer = 'Ты попал прямиком в {}'.format(city_name)
    except:
        answer = 'Котик, попробуй в следующий раз'
    bot.send_message(message.chat.id, answer)
    
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Котичек, пока я умею определять погоду в твоем городе. Просто введи название твоего города")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, '''Котичек, я умею определять погоду в твоем городе. Просто введи свой город.
    
Скрытые функции:
/btc - показывает котичку текущий курс BTC в USD''')

@bot.message_handler(commands=['contact'])
def send_welcome(message):
    answer = "Если возникли вопросы или замечания, напиши этому челику: @gyonmyon"
    bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['btc'])
def send_welcome(message):
    answer = get_btc()
    bot.send_message(message.chat.id, answer)
    

@bot.message_handler(commands=['city'])
def send_welcome(message):
    answer = "В разработке"
    bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['home'])
def send_welcome(message):
    answer = "В разработке"
    bot.send_message(message.chat.id, answer)




@bot.message_handler(func=lambda message: True)
def Send_weather(message):
    '''Send weather to answer of message.
    '''
    try:
        observation = owm.weather_at_place(message.text)
        weather = observation.get_weather()
        temperature = weather.get_temperature("celsius")["temp"]

        answer = "Сейчас в твоем городе " + weather.get_detailed_status() + "\n"
        answer += "Градусник показывает " + str(temperature) + " градусов" + "\n\n"
        if temperature < 0:
            answer += "Надевай шапку, лапуля, а то замерзнешь, лучше бы не вылазить из постели)"
        elif temperature < 10:
            answer += "На улице холодно, лучше греться теплым чаем"
        elif temperature < 15:
            answer += "Все еще можешь одеваться тепло. Жарко не будет, котик, я обещаю"
        elif temperature < 20:
            answer += "Может сегодня оденешься, по настроению, а, котичек?"
        elif temperature < 25:
            answer += "Погода шепчет, нужно выгулять котичка)))"
        elif 25 <= temperature <= 30:
            answer += "Наконец-то тепло и мне не нужно следить, чтобы котики не ходили раздетые"
        elif temperature > 30:
            answer += "Становится очень жарко, не забывай пить воду и лучше остаться дома)"
    except:
        answer = "Извини, котичек, я не понимаю("
    bot.send_message(message.chat.id, answer)

# try bot.infinity_polling(False)
#offset=lastUpdateID + 1
bot.polling(none_stop=False, interval=0, timeout=120)
