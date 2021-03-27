import telebot
from telegramcalendar import *

bot = telebot.TeleBot('1700380188:AAEUDoBpV9ATgEt-arqvYrdqcmwYi3MWmpc')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Прувет!')
    elif message.text.lower() == 'ууууууу':
        bot.send_message(message.from_user.id, 'УУУУУУУУУУУУAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAУУУУУУУУУУУУУУУУУУУУУУУУУAAAAAAAAAAAAAAAAAУУУУУУУУУУУУУУУУУУAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAУУУУУУУУУУУAAAAAAAAAAAAAAAAAAAAAAAAAAУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУ')
    elif message.text.lower() == '/start' or message.text.lower() == '/help':
        bot.reply_to(message, 'Этот бот будет присылать тебе крутую инфу про разные мероприятия ЛОЛ кринж кек!')
    elif message.text.lower() == '/calendar':
        now = datetime.datetime.now() #Текущая дата
    chat_id = message.chat.id
    date = (now.year,now.month)
    current_shown_dates[chat_id] = date #Сохраним текущую дату в словарь
    markup = create_calendar(now.year,now.month)
    bot.send_message(message.chat.id, "Пожалйста, выберите дату", reply_markup=markup)
    bot.answer_callback_query(call.id, text="Дата выбрана")
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')


bot.polling(none_stop=True)
