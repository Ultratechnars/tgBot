import telebot
import requests
import datetime
from random import randint
from telebot import types


bot = telebot.TeleBot('1700380188:AAEUDoBpV9ATgEt-arqvYrdqcmwYi3MWmpc')
age = 0
idsend = 0


def capt(words):
    words = words.split()
    for i in range(len(words)):
        if not words[i][0].isalpha():
            for j in range(len(list(words[i]))):
                if list(words[i])[j].isalpha():
                    words[i] = list(words[i])
                    words[i][j] = words[i][j].upper()
                    words[i] = ''.join(words[i])
                    break
        else:
            words[i] = words[i].capitalize()
    words = ' '.join(words)
    return words


@bot.message_handler(content_types=['text'])
def first(message):
    bot.send_message(message.from_user.id, 'Привет, я бот SPBEvents\nНапиши \'Поехали\' и я покажу тебе самые интересные события')
    bot.register_next_step_handler(message, start)


def start(message):
    if message.text == 'Поехали':
        bot.send_message(message.from_user.id, "Сколько тебе лет??")
        bot.register_next_step_handler(message, get_age)
    else:
        bot.send_message(message.from_user.id, 'Напиши \'Поехали\'')
        bot.register_next_step_handler(message, start)


def get_age(message):
    global age
    global idsend
    idsend = message.from_user.id
    if not message.text.isdigit():
        bot.send_message(message.from_user.id, 'Цифрами пожалуйста')
        bot.register_next_step_handler(message, get_age)
    else:
        age = int(message.text)
        keyboard = types.InlineKeyboardMarkup()
        key_cinema = types.InlineKeyboardButton(text='Кино🎥', callback_data='cinema')
        keyboard.add(key_cinema)
        key_concert = types.InlineKeyboardButton(text='Концерты🎵', callback_data='concert')
        keyboard.add(key_concert)
        key_education = types.InlineKeyboardButton(text='Обучение📕', callback_data='education')
        keyboard.add(key_education)
        key_exhibition = types.InlineKeyboardButton(text='Выставки🖼', callback_data='exhibition')
        keyboard.add(key_exhibition)
        key_fashion = types.InlineKeyboardButton(text='Мода и стиль💄', callback_data='fashion')
        keyboard.add(key_fashion)
        key_festival = types.InlineKeyboardButton(text='Фестивали🎊', callback_data='festival')
        keyboard.add(key_festival)
        key_kids = types.InlineKeyboardButton(text='Детям👶', callback_data='kids')
        keyboard.add(key_kids)
        key_party = types.InlineKeyboardButton(text='Вечеринки🎆', callback_data='party')
        keyboard.add(key_party)
        key_quest = types.InlineKeyboardButton(text='Квесты🚶', callback_data='quest')
        keyboard.add(key_quest)
        key_shopping = types.InlineKeyboardButton(text='Шопинг👚', callback_data='shopping')
        keyboard.add(key_shopping)
        key_theater = types.InlineKeyboardButton(text='Спектакли🎭', callback_data='theater')
        keyboard.add(key_theater)
        key_tour = types.InlineKeyboardButton(text='Экскурсии🚌', callback_data='tour')
        keyboard.add(key_tour)
        bot.send_message(message.from_user.id, text='Выбери интересующую тебя категорию', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global idsend
    categories = call.data
    if categories == 'festival':
        categories = categories + ',' + 'holiday';
    response = requests.get('https://kudago.com/public-api/v1.4/events/?lang=&fields=id,title,description,dates,place,age_restriction&expand=&order_by=&text_format=text&ids=&location=spb&actual_since=1444385206&actual_until=1444385405&page_size=100&categories=' + categories).json()
    i = randint(0, min(98, response['count']))
    try:
        placeid = response['results'][i]['place']['id']
        place = requests.get('https://kudago.com/public-api/v1.4/places/' + str(placeid) + '/?fields=title').json()[
            'title']
    except Exception:
        place = 'Место проведения неизвестно'
    age = '0+'
    if response['results'][i]['age_restriction'] is not None:
        age = str(response['results'][i]['age_restriction'])
    if age[-1] != '+':
        age += '+'
    title = response['results'][i]['title']
    title = capt(title)
    place = capt(place)
    bot.send_message(idsend, title + '\n' \
                     + response['results'][i]['description'] + '\n' \
                     + str(
        datetime.datetime.utcfromtimestamp(response['results'][i]['dates'][0]['start']).strftime('%d.%m.%y %H:%M')) \
                     + ' - ' + str(
        datetime.datetime.utcfromtimestamp(response['results'][i]['dates'][0]['end']).strftime('%d.%m.%y %H:%M')) \
                     + '\n' + place + '\n' \
                     + age)


"""def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
        response = requests.get('https://kudago.com/public-api/v1.4/events/?lang=&fields=id,title,description,dates,place,age_restriction&expand=&order_by=&text_format=text&ids=&location=spb&actual_since=1444385206&actual_until=1444385405&page_size=100').json()
        i = randint(0, 98)
        try:
            placeid = response['results'][i]['place']['id']
            place = requests.get('https://kudago.com/public-api/v1.4/places/' + str(placeid) + '/?fields=title').json()['title']
        except Exception:
            place = 'Место проведения неизвестно'
        age = '0+'
        if response['results'][i]['age_restriction'] is not None:
            age = str(response['results'][i]['age_restriction'])
        if age[-1] != '+':
            age += '+'
        title = response['results'][i]['title']
        title = capt(title)
        place = capt(place)
        bot.send_message(message.from_user.id, title + '\n' \
                        + response['results'][i]['description'] + '\n' \
                        + str(datetime.datetime.utcfromtimestamp(response['results'][i]['dates'][0]['start']).strftime('%d.%m.%y %H:%M')) \
                        + ' - ' + str(datetime.datetime.utcfromtimestamp(response['results'][i]['dates'][0]['end']).strftime('%d.%m.%y %H:%M')) \
                        + '\n' + place + '\n' \
                        + age)
    elif message.text.lower() == '/start' or message.text.lower() == '/help':
        bot.reply_to(message, 'Этот бот будет присылать тебе крутую инфу про разные мероприятия!')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')"""


if __name__ == '__main__':
    bot.polling(none_stop=True)
