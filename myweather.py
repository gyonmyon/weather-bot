from pyowm import OWM, exceptions, timeutils
import random, config
from mytoken import token, API_key   

owm = OWM(API_key, language="ua")

def get_loc_weather(latitude, longitude):
    try:
        obs = owm.weather_at_coords(latitude, longitude)
        weather = obs.get_weather()

        humidity = weather.get_humidity()
        l = obs.get_location()
        city_name = l.get_name()
        temperature = weather.get_temperature("celsius")["temp"]

        answer = "Я нашел тебя 🙈"
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
    except exceptions.api_response_error.NotFoundError:
        answer = random.choice(config.answer_NotFound)
    except exceptions.api_call_error.APICallTimeoutError:
        answer = config.answer_APICallTimeout
    
    return answer

def get_city_weather(city):
    '''Send weather of current time to answer of message.
    
    If location not found - return NotFound text'''
    try:
        obs = owm.weather_at_place(city)
        weather = obs.get_weather()
        temperature = weather.get_temperature("celsius")["temp"]
        humidity = weather.get_humidity()

        l = obs.get_location()
        city_name = l.get_name()

        fc = owm.three_hours_forecast(city)
        f = fc.get_forecast()

        answer = config.answer_text.format(city_name, weather.get_detailed_status(), temperature, humidity)
        if temperature < 0:
            answer += random.choice(config.answer_list_cold)
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
            answer += random.choice(config.answer_list_hot)
    except exceptions.api_response_error.NotFoundError:
        answer = random.choice(config.answer_NotFound)
    except exceptions.api_call_error.APICallTimeoutError:
        answer = config.answer_APICallTimeout

    return answer
