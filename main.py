import telebot

bot = telebot.TeleBot('1700380188:AAEUDoBpV9ATgEt-arqvYrdqcmwYi3MWmpc')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Прувет!')
    elif message.text.lower() == 'ууууууу':
        bot.send_message(message.from_user.id, 'УУУУУУУУУУУУ\n'
                                               'УУУУУУУУУУУУ')
    else:
        bot.send_message(message.from_user.id, 'Ничего не понимаю')


@bot.message_handler(commands=['start'])
def greetings(message):
    bot.send_message(message.from_user.id, 'Этот бот будет присылать тебе крутую инфу про разные мероприятия ЛОЛ '
                                           'кринж кек')


bot.polling(none_stop=True)
