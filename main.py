import telebot
from telebot import types
import requests

token = "5627146956:AAE2qJaGFTqfjjL39czw1E0joxLUinwuR1o"

bot = telebot.TeleBot(token)
message_to_cryptocurrency_name={'BTC': 'bitcoin', 'BNB': 'binancecoin', 'USDC': 'usd-coin', 'ETH': 'ethereum', 'USDT': 'tether'}

def get_cryptocurrency_exchange_rate():
    cryptocurrency = ['bitcoin', 'ethereum', 'tether', 'binancecoin', 'usd-coin']
    res = {}
    for c in cryptocurrency:
        res[c] = '$' + str(
            requests.get(f'https://api.coingecko.com/api/v3/coins/{c}/tickers').json()['tickers'][0]['last'])

    return res


@bot.message_handler(['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    butt1 = types.KeyboardButton("Валюты!")
    butt2 = types.KeyboardButton("Помощь!")
    markup.add(butt1, butt2)
    bot.send_message(message.chat.id, text='Привет', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Валюты!":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("BTC")
        but2 = types.KeyboardButton("ETH")
        but3 = types.KeyboardButton("USDT")
        but4 = types.KeyboardButton("BNB")
        but5 = types.KeyboardButton("USDC")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(but1, but2, but3, but4, but5, back)
        bot.send_message(message.chat.id, text="Все валюты", reply_markup=markup)


    elif message.text == "help!":
        bot.send_message(message.chat.id, text="Выбери валюту из интересующих во вкладке валюты, как нажмешь тебе высветится ее стоимость")


    elif message.text == "Вернуться в главное меню":
        bot.send_message(message.chat.id, text="Вы вернулись в меню")
        start(message)

    elif message.text in ('BTC', 'BNB', 'USDC', 'ETH', 'USDT'):
        name = message.text
        res = get_cryptocurrency_exchange_rate()[message_to_cryptocurrency_name[name]]
        bot.send_message(message.chat.id, f'курс {name}: {res}')



bot.polling(none_stop=True)

