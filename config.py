from pyowm import OWM
import mytoken

#API_key = os.environ['API_key']
API_key = mytoken.API_key
#owm = OWM(API_key) #English
owm = OWM(API_key, language="ua") #UA

reg = owm.city_id_registry()   

def guess_city():
    '''Input number to guess a city
    '''
    number = input("Input your name to choose city: ")
    obs = owm.weather_at_place(number)    
    l = obs.get_location()
    city_name = l.get_name()
    print(city_name)
    return city_name

guess_city()