# -*- coding: utf-8 -*-
import redis
import os
import telebot
import schedule
import time
import random
#host from home
#import mytoken    

# import some_api_lib
# import ...
from pyowm.exceptions import api_response_error
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
#API_key = mytoken.API_key
bot = telebot.TeleBot(token)
#              ...
# OWM API

#host from home

owm = OWM(API_key, language="ua")

@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
	pass

@bot.message_handler(regexp="(?<![\w.])[0-9]{2,4}([0-9])$")
def guess_city(message):
    '''Input number to guess a city
    '''
    try:
        observation = owm.weather_at_place(message.text)
        l = observation.get_location()
        city_name = l.get_name()
        answer = 'Ты попал прямиком в {}'.format(city_name)
    except api_response_error.NotFoundError:
        answer = 'Котик, попробуй в еще раз'
    bot.send_message(message.chat.id, answer)

sticker_list = (
    "CAADAgADAQADAcY0GmUhPCW6Bd4vAg",
    "CAADAgADggAD8jJRHB0V6PPLbjFyAg",
    "CAADAgADhAAD8jJRHLnk-jBUeuhTAg",
    "CAADAgADkQAD8jJRHIfKn60XlZdSAg",
    "CAADAgADhQAD8jJRHDNzGW-VTHq8Ag",
    "CAADAgADhwAD8jJRHI0VAW1GfrO_Ag",
    "CAADAgADgQAD8jJRHENq6dmDN1yDAg",
    "CAADAgADhgAD8jJRHKJ8teQ4pD9RAg",
    "CAADAgADhwAD8jJRHI0VAW1GfrO_Ag",
    "CAADAgADiAAD8jJRHDTXmT_B0PiCAg"
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_sticker(message.chat.id, "CAADAgADfgAD8jJRHBsycQ5qWUfNAg")
    welcome_text = '''Привет, я в твоем распоряжении 24/7. Давай расскажу что я умею. Можешь ввести название города и я скажу тебе какая погода в любом городе. Так же можешь скинуть мне свою локацию и я определю сам, где Ты находишься)
    
Все доступные функции можешь посмотреть в /help'''
    time.sleep(5)
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    help_text =  '''Котичек, я умею определять погоду в твоем городе. Просто введи свой город или отправь мне свою локацию.

/sticker - давай отправлю тебе стикер)
/contact - замечания и предложения отправляй котику, на его username

Скрытые функции:
/btc - показывает котичку текущий курс BTC в USD'''
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['sticker'])
def send_welcome(message):
    bot.send_sticker(message.chat.id, random.choice(sticker_list))

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

@bot.message_handler(content_types=['location'])
def take_location(message):
    try:
        latitude = message.location.latitude
        longitude = message.location.longitude
        obs = owm.weather_at_coords(latitude, longitude)
        weather = obs.get_weather()

        humidity = weather.get_humidity()

        l = obs.get_location()
        city_name = l.get_name()

        temperature = weather.get_temperature("celsius")["temp"]

        answer = "Я нашел тебя 🙈\n"
        answer += "Сейчас в твоем городе {} ".format(city_name) + weather.get_detailed_status() + "\n"
        answer += "Градусник показывает {}  градусов .\n".format(temperature)
        answer += "Влажность: {}%".format(humidity) + "\n\n"
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

@bot.message_handler(func=lambda message: True)
def text_message(message):
    '''Send weather to answer of message.
    '''
    try:
        obs = owm.weather_at_place(message.text)
        weather = obs.get_weather()
        temperature = weather.get_temperature("celsius")["temp"]
        humidity = weather.get_humidity()


        answer = "Сейчас в твоем городе {} ".format(city_name) + weather.get_detailed_status() + "\n"
        answer += "Градусник показывает {}  градусов \n".format(temperature)
        answer += "Влажность: {}%".format(humidity) + "\n\n"
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
bot.polling(none_stop=False, interval=0, timeout=20)
