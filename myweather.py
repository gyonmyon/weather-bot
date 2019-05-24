from pyowm import OWM, exceptions, timeutils
from config import bot
import random, config, os
from mytoken import token, API_key  
from datetime import date
from time import sleep

#API_key = os.environ['API_key']
owm = OWM(API_key, language="ua")

def get_loc_weather(latitude, longitude, message):
    try:
        obs = owm.weather_at_coords(latitude, longitude)
        weather = obs.get_weather()

        humidity = weather.get_humidity()
        l = obs.get_location()
        city_name = l.get_name()
        temperature = weather.get_temperature("celsius")["temp"]

        answer = "Я нашел тебя 🙈  \n"
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
            answer += random.choice(config.answer_list_hot)
    except exceptions.api_response_error.NotFoundError:
        bot.send_sticker(message.chat.id, config.error_sticker)
        sleep(3)
        answer = random.choice(config.answer_NotFound)
    except exceptions.api_call_error.APICallTimeoutError:
        answer = config.answer_APICallTimeout
    except exceptions.api_call_error.APICallError:
        answer = config.answer_APICallError

    return answer

def get_city_weather(city):
    '''Send weather of current time to answer of message.
    
    If location not found - return NotFound text
    If timeout reached - return Timeout text'''
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
        sleep(3)
        answer = random.choice(config.answer_NotFound)
    except exceptions.api_call_error.APICallTimeoutError:
        answer = config.answer_APICallTimeout
    except exceptions.api_call_error.APICallError:
        answer = config.answer_APICallError

    return answer


def get_moc_weather(latitude, longitude):
    try:
        obs = owm.weather_at_coords(latitude, longitude)
        weather = obs.get_weather()

        humidity = weather.get_humidity()
        l = obs.get_location()
        city_name = l.get_name()
        temperature = weather.get_temperature("celsius")["temp"]
        fc = owm.three_hours_forecast(city_name)
        f = fc.get_forecast()
        lst = f.get_weathers()[0:2]
        today = (date.today)

        tr = timeutils.next_three_hours()


        start = lst.when_starts('iso')
        finish = lst.when_ends('iso')    
     
        print(fc.get_weather_at())
        #print(lst.when_starts)
        if fc.will_have_snow():
            print("СНІГ")
        elif fc.will_have_rain():
            print("Можливий дощ")
        elif fc.will_have_rain() and fc.will_have_clouds():
            print("Хмарно. Можливий дощ.")
        elif fc.will_have_sun():
            print("Сонячно")
        elif fc.will_have_fog():
            print("Туманно")
    except:
        pass

def get_forecasts(city):
    obs = owm.weather_at_place(city)
    fc = owm.three_hours_forecast(city)
    f = fc.get_forecast()
# Get the list of Weather objects...
    #lst = f.get_weathers()[0:2] #for +3 +6 h
    #print(lst)
    temp, humid, sts = [], [], []

    for weather in f:
        temp.append(weather.get_temperature("celsius")["temp"])	
        humid.append(weather._humidity)
        sts.append(weather._detailed_status)
        #
        #weather.current
        print(f.get_reception_time('iso'))
        if len(temp) == 3:
            break
    answer = '''Через три години: Температура {}
Вологість: {}%
Буде {}'''.format( temp[0], humid[0], sts[0])
    print(answer)
    return answer

if __name__ == "__main__":
    get_moc_weather(50, 20)
    get_forecasts("Бориспіль")
    
    