# -*- coding: utf-8 -*-
import redis
import json
import os
from telebot import TeleBot, types
import schedule
import time
import random
import config
from myweather import get_loc_weather, get_city_weather

#host from home
from mytoken import token, API_key   

# import some_api_lib
from pyowm import OWM, exceptions, timeutils
#Yobit function
from yobit import get_btc

#           Config vars
#token = os.environ['TELEGRAM_TOKEN']
#API_key = os.environ['API_key']

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
# r = redis.from_url(os.environ.get("REDIS_URL"))
bot = TeleBot(token)
owm = OWM(API_key, language="ua")
#              ...

@bot.message_handler(content_types=['audio'])
def handle_docs_audio(message):
    bot.send_message(message.chat.id, config.answer_audio)

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
        guess_answer = config.answer_NotFound
    except exceptions.api_call_error.APICallTimeoutError:
        bot.send_sticker(message.chat.id, config.timeout_sticker)
        time.sleep(5)
        guess_answer = config.answer_APICallTimeout
    bot.send_message(message.chat.id, guess_answer)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_sticker(message.chat.id, config.start_sticker)
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
    bot.send_message(message.chat.id, config.answer_contact)

@bot.message_handler(commands=['btc'])
def send_welcome(message):
    answer = get_btc()
    bot.send_message(message.chat.id, answer)
    
@bot.message_handler(commands=['city'])
def send_welcome(message):
    bot.send_message(message.chat.id, config.answer_dev)

@bot.message_handler(commands=['home'])
def send_welcome(message):
    bot.send_message(message.chat.id, config.answer_dev)

@bot.message_handler(content_types=['location'])
def take_location(message):
    #print(message.json['date'])

    latitude = message.location.latitude
    longitude = message.location.longitude
    bot.send_message(message.chat.id, get_loc_weather(latitude, longitude))
    
@bot.message_handler(func=lambda message: True)
def text_message(message):    
    bot.send_message(message.chat.id, get_city_weather(message.text))

bot.polling(none_stop=False, interval=0, timeout=20)