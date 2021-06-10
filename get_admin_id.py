import telebot

BOT_TOKEN = ""

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def get_id(message):
    bot.send_message(message.chat.id, text="_Your ADMIN_ID is {}._".format(message.chat.id), parse_mode="Markdown")
