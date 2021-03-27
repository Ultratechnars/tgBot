import telebot
import requests
import datetime
from random import randint


bot = telebot.TeleBot('1700380188:AAEUDoBpV9ATgEt-arqvYrdqcmwYi3MWmpc')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
        response = requests.get('https://kudago.com/public-api/v1.4/events/?lang=&fields=id,title,description,dates,place,age_restriction&expand=&order_by=&text_format=text&ids=&location=spb&actual_since=1444385206&actual_until=1444385405&page_size=100').json()
        i = randint(0, 100)
        try:
            placeid = response['results'][i]['place']['id']
            place = requests.get('https://kudago.com/public-api/v1.4/places/' + str(placeid) + '/?fields=title').json()['title']
        except Exception:
            place = 'Место проведения неизвестно'
        bot.send_message(message.from_user.id, response['results'][i]['title'].capitalize() + '\n' \
                        + response['results'][i]['description'] + '\n' \
                        + str(datetime.datetime.utcfromtimestamp(response['results'][i]['dates'][0]['start']).strftime('%d.%m.%y %H:%M')) \
                        + ' - ' + str(datetime.datetime.utcfromtimestamp(response['results'][i]['dates'][0]['end']).strftime('%d.%m.%y %H:%M')) \
                        + '\n' + place.capitalize() + '\n' \
                        + 'Ограничение: ' +str(response['results'][i]['age_restriction']+'+'))
    elif message.text.lower() == '/start' or message.text.lower() == '/help':
        bot.reply_to(message, 'Этот бот будет присылать тебе крутую инфу про разные мероприятия!')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')


if __name__ == '__main__':
    bot.polling(none_stop=True)
