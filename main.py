import telebot
from telebot import types


bot = telebot.TeleBot('1700380188:AAEUDoBpV9ATgEt-arqvYrdqcmwYi3MWmpc')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Прувет!')
    elif message.text.lower() == 'УУУУ':
        bot.send_message(message.from_user.id, 'УУУУУУУУУУУУ\n'
                                               'УУУУУУУУУУУУУффф')
    else:
        bot.send_message(message.from_user.id, 'Ничего не понимаю')
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    keyboard = types.InlineKeyboardMarkup()
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)


def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Запомню : )')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Запомню : )')


@bot.message_handler(commands=['start'])
def greetings(message):
    bot.send_message(message.from_user.id, 'Этот бот будет присылать тебе крутую инфу про разные мероприятия ЛОЛ '
                                           'кринж кек')


bot.polling(none_stop=True)
