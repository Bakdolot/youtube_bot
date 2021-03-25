import os
from telebot import *
from pytube import YouTube
bot = TeleBot('сюда ставится наш ключ')
@bot.message_handler(commands='start', content_types='text')
def start_bot(message):
    global Chat_id
    Chat_id = message.chat.id
    try:
        keyboard = types.InlineKeyboardMarkup()
        mp3 = types.InlineKeyboardButton(text='Аудио', callback_data='mp3')
        keyboard.add(mp3)
        mp4 = types.InlineKeyboardButton(text='Видео файл', callback_data='mp4')
        keyboard.add(mp4)
        bot.send_message(Chat_id, 'Привет это бот для скачивание видео или аудио файлов с ютуба. \nВыберите формат для скачивание', reply_markup=keyboard)
    except:
        bot.send_message(Chat_id, 'xm')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'mp3':
        a = bot.send_message(Chat_id, 'Вставьте ссылку видео')
        bot.register_next_step_handler(a, mp3_downloader)
    elif call.data == 'mp4':
        a = bot.send_message(Chat_id, 'Вставьте ссылку видео')
        bot.register_next_step_handler(a, mp4_downloader)
def mp3_downloader(message):
    try:
        YouTube(message.text).streams.get_audio_only().download()
        a = bot.send_message(Chat_id, 'загрузка началось')
        b = f'{os.getcwd()}\{YouTube(message.text).title}.mp4'
        os.replace(b, f'{os.getcwd()}\{YouTube(message.text).title}.mp3')
        c = open(f'{os.getcwd()}\{YouTube(message.text).title}.mp3', 'rb')
        bot.send_audio(Chat_id, c)
        os.remove(f'{os.getcwd()}\{YouTube(message.text).title}.mp3')
        bot.register_next_step_handler(a, start_bot)
    except:
        a = bot.send_message(Chat_id, 'Введите ссылку коректно')
        bot.register_next_step_handler(a, mp3_downloader)

def mp4_downloader(message):
    try:
        bot.send_message(Chat_id, 'загрузка началось')
        YouTube(message.text).streams.get_highest_resolution().download()
        a = bot.send_message(Chat_id, 'загрузка закончилось')
        b = open(f'{os.getcwd()}\{YouTube(message.text).title}.mp4', 'rb')
        bot.send_video(Chat_id, b)
        os.remove(f'{os.getcwd()}\{YouTube(message.text).title}.mp4')
        bot.register_next_step_handler(a, start_bot)
    except:
        a = bot.send_message(Chat_id, 'Введите ссылку коректно')
        bot.register_next_step_handler(a, mp4_downloader)
# @bot.message_handler(content_types=['text'])
# def send_welcome(message):
#     global Chat_id
#     Chat_id = message.chat.id
#     # a = bot.send_message(Chat_id, '')
#     bot.send_message('если хочеш еще скачать что нибудь нажми на /start')

bot.polling(none_stop=True, timeout=123)