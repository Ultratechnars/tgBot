import telebot
import requests
from random import randint

bot = telebot.TeleBot('1700380188:AAEUDoBpV9ATgEt-arqvYrdqcmwYi3MWmpc')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Прувет!')
        response = requests.get('https://kudago.com/public-api/v1.4/events/?lang=&fields=&expand=&order_by=&text_format=text&ids=&location=&actual_since=1444385206&actual_until=1444385405&is_free=&lon=&lat=&radius=').json()
        bot.send_message(message.from_user.id, response['results'][randint(0, 20)]['title'])
    elif message.text.lower() == 'ууууууу':
        bot.send_message(message.from_user.id, 'УУУУУУУУУУУУAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAУУУУУУУУУУУУУУУУУУУУУУУУУAAAAAAAAAAAAAAAAAУУУУУУУУУУУУУУУУУУAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAУУУУУУУУУУУAAAAAAAAAAAAAAAAAAAAAAAAAAУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУ')
    elif message.text.lower() == '/start' or message.text.lower() == '/help':
        bot.reply_to(message, 'Этот бот будет присылать тебе крутую инфу про разные мероприятия ЛОЛ кринж кек!')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')


bot.polling(none_stop=True)
