import telebot
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE
import requests
import datetime
from random import randint
from telebot import types

calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")
bot = telebot.TeleBot('1700380188:AAEUDoBpV9ATgEt-arqvYrdqcmwYi3MWmpc')
ages = {}
used = {}
dates = {}


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
        keyboard.row("Сегодня")
        keyboard.row("Завтра")
        keyboard.row("Выбрать дату")
        bot.send_message(message.from_user.id, text='Когда вы хотите поехать?', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_date)


def get_date(message):
    if message.text == "Сегодня":
        dates[str(message.from_user.id)] = datetime.date.today()
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('Кино🎥', 'Концерты🎵', 'Обучение📕')
        keyboard.row('Выставки🖼', 'Мода и стиль💄', 'Фестивали🎊')
        keyboard.row('Детям👶', 'Квесты🚶')
        keyboard.row('Спектакли🎭', 'Экскурсии🚌')
        bot.send_message(message.from_user.id, text='Выберите интересующую тебя категорию', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_event)
    elif message.text == "Завтра":
        dates[str(message.from_user.id)] = datetime.date.today() + datetime.timedelta(days = 1)
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('Кино🎥', 'Концерты🎵', 'Обучение📕')
        keyboard.row('Выставки🖼', 'Мода и стиль💄', 'Фестивали🎊')
        keyboard.row('Детям👶', 'Квесты🚶')
        keyboard.row('Спектакли🎭', 'Экскурсии🚌')
        bot.send_message(message.from_user.id, text='Выберите интересующую тебя категорию', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_event)
    else:
        now = datetime.datetime.now()  # Get the current date
        bot.send_message(
            message.chat.id,
            "Selected date",
            reply_markup=calendar.create_calendar(
                name=calendar_1_callback.prefix,
                year=now.year,
                month=now.month,  # Specify the NAME of your calendar
            ),
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1_callback.prefix))
def callback_inline(call):
# At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
# Processing the calendar. Get either the date or None if the buttons are of a different type
    date = calendar.calendar_query_handler(bot=bot, call=call, name=name, action=action, year=year, month=month, day=day)
# There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
    if action == "DAY":
        dates[str(call.from_user.id)] = datetime.date(year = int(year), month = int(month), day = int(day))
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('Кино🎥', 'Концерты🎵', 'Обучение📕')
        keyboard.row('Выставки🖼', 'Мода и стиль💄', 'Фестивали🎊')
        keyboard.row('Детям👶', 'Квесты🚶')
        keyboard.row('Спектакли🎭', 'Экскурсии🚌')
        bot.send_message(call.from_user.id, text='Выберите интересующую тебя категорию', reply_markup=keyboard)
        bot.register_next_step_handler(call.message, get_event)
    elif action == "CANCEL":
        bot.send_message(call.from_user.id, text='Отменяю')
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row("Сегодня")
        keyboard.row("Завтра")
        keyboard.row("Выбрать дату")
        bot.send_message(call.from_user.id, text='Когда вы хотите поехать?', reply_markup=keyboard)
        bot.register_next_step_handler(call.message, get_date)



def get_event(message):
    categories = ''
    startdate = dates[str(message.from_user.id)]
    startutc = datetime.datetime(year = startdate.year - 1, month = 1, day = 1)
    startutc = datetime.datetime.timestamp(startutc)
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
    elif message.text == 'Квесты🚶':
        categories = 'quest'
    elif message.text == 'Спектакли🎭':
        categories = 'theater'
    elif message.text == 'Экскурсии🚌':
        categories = 'tour'
    response = requests.get(
        'https://kudago.com/public-api/v1.4/events/?lang=&fields=id,title,description,dates,place,age_restriction,images,site_url&expand=&order_by=&text_format=text&ids=&location=spb&actual_since=' + str(startutc) + '&page_size=100&categories=' + categories).json()
    if response['count'] == 0:
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('Кино🎥', 'Концерты🎵', 'Обучение📕')
        keyboard.row('Выставки🖼', 'Мода и стиль💄', 'Фестивали🎊')
        keyboard.row('Детям👶', 'Квесты🚶')
        keyboard.row('Спектакли🎭', 'Экскурсии🚌')
        bot.send_message(message.from_user.id, text='Ничего нет, увы. Попробуйте другую категорию', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_event)
        return
    res = []
    res += response['results']
    while response['next']:
        response = requests.get(response['next']).json()
        res += response['results']
    i = 0
    if len(res) == 0:
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('Кино🎥', 'Концерты🎵', 'Обучение📕')
        keyboard.row('Выставки🖼', 'Мода и стиль💄', 'Фестивали🎊')
        keyboard.row('Детям👶', 'Квесты🚶')
        keyboard.row('Спектакли🎭', 'Экскурсии🚌')
        bot.send_message(message.from_user.id, text='Ничего нет, увы. Попробуйте другую категорию',
                         reply_markup=keyboard)
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
            endd = datetime.date(end.year, end.month, end.day)
            starte = datetime.datetime.fromtimestamp(z['start'])
            startd = datetime.date(starte.year, starte.month, starte.day)
            if endd >= startdate >= startd:
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
        place = ''
    title = res[i]['title']
    title = capt(title)
    place = capt(place) + '\n'
    imgsrc = res[i]['images'][0]['image']
    img = requests.get(imgsrc)
    if message.from_user.id not in used:
        used[str(message.from_user.id)] = [res[i]['id']]
    else:
        used[str(message.from_user.id)].append(res[i]['id'])
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row("Сегодня")
    keyboard.row("Завтра")
    keyboard.row("Выбрать дату")
    bot.register_next_step_handler(message, get_date)
    bot.send_photo(message.from_user.id, img.content, title + '\n' \
                     + res[i]['description'] + '\n' \
                     + str(
        datetime.datetime.utcfromtimestamp(res[i]['dates'][0]['start']).strftime('%d.%m.%Y %H:%M')) \
                     + ' - ' + str(
        datetime.datetime.utcfromtimestamp(res[i]['dates'][0]['end']).strftime('%d.%m.%Y %H:%M')) \
                     + '\n' + place + res[i]['site_url'] + '\n' + 'Когда хотите поехать в следующий раз?', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_date)
    return


if __name__ == '__main__':
    bot.polling(none_stop=True)
