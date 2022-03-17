import telebot
from config import TOKEN, keys
from extensions import Convertor, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    announcing = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
    <в какую валюту перевести> \
    <количество переводимой валюты>\nУвидить список всех доступных валют: /values'
    bot.reply_to(message, announcing)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    announcing = 'Доступные валюты:'
    for key in keys.keys():
        announcing = '\n'.join((announcing, key, ))
    bot.reply_to(message, announcing)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        split_string = message.text.split(' ')
        if len(split_string) != 3:
            raise APIException('Некорретный формат вводных данных.')
        quote, base, amount = split_string
        total_base = Convertor.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду. \n{e}')
    else:
        announcing = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, announcing)

bot.polling()