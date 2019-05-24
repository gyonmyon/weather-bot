import os
from telebot import TeleBot, types
from mytoken import token

#token = os.environ['TELEGRAM_TOKEN']
bot = TeleBot(token)

help_text =  '''Котичек, я умею определять погоду в твоем городе. Просто введи свой город или отправь мне свою локацию.

/sticker - давай отправлю тебе стикер)
/contact - замечания и предложения отправляй котику, на его username

Скрытые функции:
/btc - показывает котичку текущий курс BTC в USD'''

welcome_text = '''Привет, я в твоем распоряжении 24/7. Давай расскажу что я умею. Можешь ввести название города и я скажу тебе какая погода в любом городе. Также можешь скинуть мне свою локацию и я определю сам, где Ты находишься)
    
Все доступные функции можешь посмотреть в /help'''

sticker_list = (
    "CAADAgADfgAD8jJRHBsycQ5qWUfNAg",
    "CAADAgADkgAD8jJRHGU0BGG5fiOiAg",
    'CAADAgADkwAD8jJRHC9MPI-Y7TsBAg', # Ошибочка
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
start_sticker = sticker_list[0]
timeout_sticker = sticker_list[1]
error_sticker = sticker_list[2]

# try bot.infinity_polling(False)
#offset=lastUpdateID + 1
answer_text = '''Сейчас в твоем городе {}: {}
Градусник показывает {} градусов
Влажность: {}% \n
'''
answer_dev = 'В разработке'

answer_contact = "Если возникли вопросы или замечания, напиши этому челику: @gyonmyon"

answer_audio = "Спасибо котик, обязательно послушаю"

answer_list_cold = (
    'Надевай шапку, лапуля, а то замерзнешь, лучше бы не вылазить из постели)',
    "Тебе там не холодно, котичка?",
)

#temp > 30
answer_list_hot = (
    'Если ты на улице то лучше быть в тени. И не забывай пить воду 🐈',
    'Котик, пойдем загорать?',
    'Становится очень жарко, не забывай пить воду и лучше остаться дома)'      
)

answer_NotFound = (
    'Почему-то не находит(',
    'Котик, попробуй еще раз',
    'Пишет, что такого города не существует)'
)

answer_APICallTimeout = (
    'Сервер как-то долго отвечает, ждем ответа',
)

answer_APICallError = (
    'Ошибочка с соединением котика, ответственного за погоду, повтори еще раз.'
)