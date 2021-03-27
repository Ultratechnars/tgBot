import telebot
import requests
import datetime
from random import randint
from telebot import types


bot = telebot.TeleBot('1700380188:AAEUDoBpV9ATgEt-arqvYrdqcmwYi3MWmpc')
ages = {}
used = {}


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
        bot.send_message(message.from_user.id, "Сколько тебе лет?")
        bot.register_next_step_handler(message, get_age)
    else:
        bot.send_message(message.from_user.id, 'Напиши \'Поехали\'')
        bot.register_next_step_handler(message, start)


def get_age(message):
    global age
    if not message.text.isdigit():
        bot.send_message(message.from_user.id, 'Цифрами пожалуйста')
        bot.register_next_step_handler(message, get_age)
    else:
        age = int(message.text)
        ages[str(message.from_user.id)] = age
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('Кино🎥', 'Концерты🎵', 'Обучение📕')
        keyboard.row('Выставки🖼', 'Мода и стиль💄', 'Фестивали🎊')
        keyboard.row('Детям👶', 'Вечеринки🎆', 'Квесты🚶')
        keyboard.row('Спектакли🎭', 'Экскурсии🚌')
        bot.send_message(message.from_user.id, text='Выбери интересующую тебя категорию', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_event)


def get_event(message):
    categories = ''
    now = datetime.date.today()
    startdate = now + datetime.timedelta(days = 1)
    time = datetime.time(0, 0, 0, 0)
    startdate = datetime.datetime.combine(startdate, time)
    if message.text == 'Кино🎥':
        categories = 'cinema'
    elif message.text == 'Концерты🎵':
        categories = 'concert'
    elif message.text == 'Обучение📕':
        categories = 'education'
    elif message.text == 'Выставки🖼':
        categories = 'exhibition'
    elif message.text == 'Мода и стиль💄':
        categories = 'fashion'
    elif message.text == 'Фестивали🎊':
        categories = 'festival,holiday'
    elif message.text == 'Детям👶':
        categories = 'kids'
    elif message.text == 'Вечеринки🎆':
        categories = 'party'
    elif message.text == 'Квесты🚶':
        categories = 'quest'
    elif message.text == 'Спектакли🎭':
        categories = 'theater'
    elif message.text == 'Экскурсии🚌':
        categories = 'tour'
    response = requests.get(
        'https://kudago.com/public-api/v1.4/events/?lang=&fields=id,title,description,dates,place,age_restriction,images,site_url&expand=&order_by=&text_format=text&ids=&location=spb&actual_since=1444385206&actual_until=1444385405&page_size=100&categories=' + categories).json()
    if response['count'] == 0:
        bot.send_message(message.from_user.id, 'Ничего нет, увы. Попробуйте другую категорию!')
        bot.register_next_step_handler(message, get_event)
        return
    res = []
    res += response['results']
    while response['next']:
        response = requests.get(response['next']).json()
        res += response['results']
    i = 0
    if len(res) == 0:
        bot.send_message(message.from_user.id, 'Ничего нет, увы. Попробуйте другую категорию!')
        bot.register_next_step_handler(message, get_event)
        return
    ok = False
    while not ok:
        i = randint(0, len(res) - 1)
        ok = False
        for z in res[i]['dates']:
            if z['start'] < 0:
                z['start'] = 0
            if z['end'] > 2145916800:
                z['end'] = 2145916800
            end = datetime.datetime.fromtimestamp(z['end'])
            starte = datetime.datetime.fromtimestamp(z['start'])
            if end.month > startdate.month > starte.month:
                ok = True
                break
            elif (startdate.month == end.month and startdate.day <= end.day) or (startdate.month == starte.month and startdate.day >= starte.day):
                ok = True
                break
        if str(message.from_user.id) in used:
            for j in used[str(message.from_user.id)]:
                if j == res[i]['id']:
                    ok = False
        if res[i]['age_restriction'] is not None:
            agestr = str(res[i]['age_restriction'])
            ager = 0
            for j in agestr:
                if j.isdigit():
                    ager *= 10
                    ager += int(j)
            agecheck = ages[str(message.from_user.id)]
            if agecheck < ager:
                ok = False
    try:
        placeid = res[i]['place']['id']
        place = requests.get('https://kudago.com/public-api/v1.4/places/' + str(placeid) + '/?fields=title').json()[
            'title']
    except Exception:
        place = 'Место проведения неизвестно'
    title = res[i]['title']
    title = capt(title)
    place = capt(place)
    imgsrc = res[i]['images'][0]['image']
    img = requests.get(imgsrc)
    if message.from_user.id not in used:
        used[str(message.from_user.id)] = [res[i]['id']]
    else:
        used[str(message.from_user.id)].append(res[i]['id'])
    bot.send_photo(message.from_user.id, img.content, title + '\n' \
                     + res[i]['description'] + '\n' \
                     + str(
        datetime.datetime.utcfromtimestamp(res[i]['dates'][0]['start']).strftime('%d.%m %H:%M')) \
                     + ' - ' + str(
        datetime.datetime.utcfromtimestamp(res[i]['dates'][0]['end']).strftime('%d.%m %H:%M')) \
                     + '\n' + place + '\n' + res[i]['site_url'])

    return


if __name__ == '__main__':
    bot.polling(none_stop=True)
