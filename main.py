import telebot

bot = telebot.TeleBot('1700380188:AAEUDoBpV9ATgEt-arqvYrdqcmwYi3MWmpc')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Ghbdtn')
    elif message.text.lower() == '/start' or message.text.lower() == '/help':
        bot.reply_to(message, 'Этот бот будет присылать тебе крутую инфу про разные мероприятия ЛОЛ кринж кек!')   
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')
if __name__ == '__main__':
    bot.polling(none_stop=True)
