import telebot
from telebot import types
import utils

bot = telebot.TeleBot('1700380188:AAEUDoBpV9ATgEt-arqvYrdqcmwYi3MWmpc')

@bot.message_handler(commands=['start'])
def start_menu(message):
    message_text = 'Здравствуйте!\n' \
                    + 'Наберите /help - для отображения списка доступных команд.'
    bot.send_message(message.chat.id, message_text)

@bot.message_handler(commands=['help'])
def print_menu(message):
    message_text = 'Вот, что умеет этот бот:\n' \
                    + '/help - отображает список доступных команд\n' \
                    + '/read_rss - присылает сводную информацию из выбранных источников'
    bot.send_message(message.chat.id, message_text)

@bot.message_handler(commands=['read_rss'])
def read_rss(message):
    post = utils.feed_parser()
    bot.send_message(message.chat.id, 'Новая информация на выбранных площадках:')
    for key in post.keys():
        bot.send_message(message.chat.id, key + '\n' + post[key])

if __name__ == '__main__':
    bot.infinity_polling()
