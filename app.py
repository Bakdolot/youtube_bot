import os
from telebot import *
from pytube import YouTube
bot = TeleBot('1775667238:AAENhbWI_bWVNhRYgmafbU_ClLtQ9ydkQRo')
Chat_id = ''
flag = 0
@bot.message_handler(commands=['start'], content_types=['text'])
def start_bot(message):
    global Chat_id
    Chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    mp3 = types.InlineKeyboardButton(text='Аудио', callback_data='mp3')
    keyboard.add(mp3)
    mp4 = types.InlineKeyboardButton(text='Видео файл', callback_data='mp4')
    keyboard.add(mp4)
    bot.send_message(Chat_id, 'Привет это бот для скачивание видео или аудио файлов с ютуба. \nВыберите формат для скачивание', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global flag
    if call.data == 'mp3':
        a = bot.send_message(Chat_id, 'Вставьте ссылку аудио')
        flag = 0
        bot.register_next_step_handler(a, mp3_downloader)
    elif call.data == 'mp4':
        a = bot.send_message(Chat_id, 'Вставьте ссылку видео')
        flag = 1
        bot.register_next_step_handler(a, mp4_downloader)
def mp3_downloader(message):
    try:
        if flag == 1:
            return
        yt = YouTube(message.text)
        YouTube(message.text).streams.get_audio_only().download()
        a = bot.send_message(Chat_id, 'загрузка началось')
        b = f'{os.getcwd()}\{YouTube(message.text).title}.mp4'
        d = os.replace(b, f'{os.getcwd()}\{YouTube(message.text).title}.mp3')
        c = open(f'{os.getcwd()}\{YouTube(message.text).title}.mp3', 'rb')
        bot.send_audio(Chat_id, c)
        bs = f'{os.getcwd()}\{yt.title}.mp3'
        c.close()
        os.remove(bs)
        bot.register_next_step_handler(a, start_bot)
    except:
        a = bot.send_message(Chat_id, 'Введите ссылку коректно')
        bot.register_next_step_handler(a, mp3_downloader)

def mp4_downloader(message):
    try:
        if flag == 0:
            return
        yt = YouTube(message.text)
        yt.streams.get_highest_resolution().download()
        a = bot.send_message(Chat_id, 'загрузка закончилось')
        b = open(f'{os.getcwd()}\{yt.title}.mp4', 'rb')
        bot.send_video(Chat_id, b)
        b.close()
        os.remove(f'{os.getcwd()}\{yt.title}.mp4')
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