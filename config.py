help_text =  '''Котичек, я умею определять погоду в твоем городе. Просто введи свой город или отправь мне свою локацию.

/sticker - давай отправлю тебе стикер)
/contact - замечания и предложения отправляй котику, на его username

Скрытые функции:
/btc - показывает котичку текущий курс BTC в USD'''

welcome_text = '''Привет, я в твоем распоряжении 24/7. Давай расскажу что я умею. Можешь ввести название города и я скажу тебе какая погода в любом городе. Так же можешь скинуть мне свою локацию и я определю сам, где Ты находишься)
    
Все доступные функции можешь посмотреть в /help'''

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

# try bot.infinity_polling(False)
#offset=lastUpdateID + 1
answer_text = '''Сейчас в твоем городе {}: {}
Градусник показывает {} градусов
Влажность: {}%
'''