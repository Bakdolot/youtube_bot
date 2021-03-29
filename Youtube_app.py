import telebot

TOKEN ='1761734059:AAFMOx_oBDPq2w_F-GRMqj-pKeGXcqHaoYU'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome!")

@bot.message_handler(commands=['start_game'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, " Отправьте мне ссылку видео для скачивания")
    bot.register_next_step_handler(msg, game_handler)