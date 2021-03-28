import telebot
import requests
import datetime
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE
from random import randint
from telebot import types


bot = telebot.TeleBot('1700380188:AAEUDoBpV9ATgEt-arqvYrdqcmwYi3MWmpc')

ages = {}
used = {}
dates = {}

calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")

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


def get_date(message):
    if message.text == "Сегодня":
        dates[str(message.from_user.id)] = datetime.date.today()
    elif message.text == "Завтра":
        dates[str(message.from_user.id)] = datetime.date.today() + datetime.timedelta(days = 1)
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
        # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
        name, action, year, month, day = call.data.split(calendar_1_callback.sep)
        # Processing the calendar. Get either the date or None if the buttons are of a different type
        date = calendar.calendar_query_handler(
            bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
        )
        # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
        if action == "DAY":
            bot.send_message(
                chat_id=call.from_user.id,
                text=f"You have chosen {date.strftime('%d.%m.%Y')}",
                reply_markup=ReplyKeyboardRemove(),
            )
            print(f"{calendar_1_callback}: Day: {date.strftime('%d.%m.%Y')}")
        elif action == "CANCEL":
            bot.send_message(
                chat_id=call.from_user.id,
                text="Cancellation",
                reply_markup=ReplyKeyboardRemove(),
            )
            print(f"{calendar_1_callback}: Cancellation")
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row('Кино🎥', 'Концерты🎵', 'Обучение📕')
    keyboard.row('Выставки🖼', 'Мода и стиль💄', 'Фестивали🎊')
    keyboard.row('Детям👶', 'Квесты🚶')
    keyboard.row('Спектакли🎭', 'Экскурсии🚌')
    bot.send_message(message.from_user.id, text='Выберите интересующую тебя категорию', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_event)


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
            'title'] + '\n'
    except Exception:
        place = ''
    title = res[i]['title']
    title = capt(title)
    place = capt(place)
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
    bot.send_message(message.from_user.id, text='Когда ты хочешь пойти?', reply_markup=keyboard)
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


bot.polling(none_stop=True)
