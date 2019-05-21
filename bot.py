# -*- coding: utf-8 -*-
import redis
import json
import os
import telebot
from telebot import types
import schedule
import time
import random
import config

#host from home
#from mytoken import token, API_key   

# import some_api_lib
from pyowm import OWM, exceptions, timeutils
#Yobit function
from yobit import get_btc

# Example of your code beginning
#           Config vars
token = os.environ['TELEGRAM_TOKEN']
API_key = os.environ['API_key']

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
# r = redis.from_url(os.environ.get("REDIS_URL"))

bot = telebot.TeleBot(token)

owm = OWM(API_key, language="ua")
#              ...

@bot.message_handler(content_types=['audio'])
def handle_docs_audio(message):
    answer_audio = "Спасибо котик, обязательно послушаю"
    bot.send_message(message.chat.id, answer_audio)

@bot.message_handler(regexp="(?<![\w.])[0-9]{2,4}([0-9])$")
def guess_city(message):
    '''Return city name by a number
    
    If city not found - return NotFoundError
    If Timeout is reached - return APICallTimeoutError'''
    try:
        obs = owm.weather_at_place(message.text)
        l = obs.get_location()
        city_name = l.get_name()
        guess_answer = 'Ты попал прямиком в {}'.format(city_name)
    except exceptions.api_response_error.NotFoundError:
        guess_answer = 'Котик, попробуй еще раз'
    except exceptions.api_call_error.APICallTimeoutError:
        timeout_sticker = 'CAADAgADkgAD8jJRHGU0BGG5fiOiAg'
        bot.send_sticker(message.chat.id, timeout_sticker)
        time.sleep(5)
        guess_answer = 'Сервер как-то долго отвечает, ждем ответа'
    bot.send_message(message.chat.id, guess_answer)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    start_sticker = "CAADAgADfgAD8jJRHBsycQ5qWUfNAg"
    bot.send_sticker(message.chat.id, start_sticker)
    time.sleep(5)
    bot.send_message(message.chat.id, config.welcome_text)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, config.help_text)

@bot.message_handler(commands=['sticker'])
def send_sticker(message):
    bot.send_sticker(message.chat.id, random.choice(config.sticker_list))

@bot.message_handler(commands=['contact'])
def send_contact(message):
    answer_contact = "Если возникли вопросы или замечания, напиши этому челику: @gyonmyon"
    bot.send_message(message.chat.id, answer_contact)

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
    #print(message.json['date'])
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
        answer += config.answer_text.format(city_name, weather.get_detailed_status(), temperature, humidity)
        if temperature < 0:
            answer += "Тебе там не холодно, котичка?"
        elif temperature < 10:
            answer += "Чашка горячего чая не помешает"
        elif temperature < 15:
            answer += "Чуууточку бы теплее)"
        elif temperature < 20:
            answer += "Муур"
        elif temperature < 25:
            answer += "Погода шепчет, нужно выгулять котичка)))"
        elif 25 <= temperature <= 30:
            answer += "Еще чуть-чуть и станет совсем жарко, раздевайся...))"
        elif temperature > 30:
            answer += "Если ты на улице то лучше быть в тени. И не забывай пить воду 🐈"
    except:
        answer = "Извини, котичек, я не понимаю("
    
    bot.send_message(message.chat.id, answer)

@bot.message_handler(func=lambda message: True)
def text_message(message):
    '''Send weather of current time to answer of message.
    
    If location not found - return NotFound text'''
    try:
        obs = owm.weather_at_place(message.text)
        weather = obs.get_weather()
        temperature = weather.get_temperature("celsius")["temp"]
        humidity = weather.get_humidity()

        l = obs.get_location()
        city_name = l.get_name()

        fc = owm.three_hours_forecast(message.text)
        f = fc.get_forecast()

        answer = config.answer_text.format(city_name, weather.get_detailed_status(), temperature, humidity)
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

bot.polling(none_stop=False, interval=0, timeout=20)