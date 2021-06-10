from pytube import YouTube
import telebot
import os
from threading import Thread
import time


BOT_TOKEN = '' # Token you get from BotFather in Telegram
ADMIN_ID = 0 # Administrator ID(chat_id)
ADMIN_LINK = "" # Here is link to message you in Telegram
bot = telebot.TeleBot(BOT_TOKEN)
users_per_day = []
users_per_hour = []
errors_per_day = []
day_count = time.strftime("%d")
hour_count = time.strftime("%H")

def count_users():
    global day_count, hour_count, users_per_hour, users_per_day, errors_per_day
    while True:
        if day_count != time.strftime("%d"):
            file = open(time.strftime("%d-%m-%Y-log.txt"), 'w')
            file.write("Today bot have been used by {0} people.\nAmount of errors {1}:\n".format(len(users_per_day), len(errors_per_day)))
            for error in errors_per_day:
                file.write(error + "\n")
            file.close()
            file = open(time.strftime("%d-%m-%Y-log.txt"), 'rb')
            bot.send_document(ADMIN_ID, file)
            file.close()
            users_per_day = []
            day_count = time.strftime("%d")
        if hour_count != time.strftime("%H"):
            users_per_hour = []
            hour_count = time.strftime("%H")
        time.sleep(5)


def get_url(message):
    try:
        url = message.text
        video = YouTube(url)
        bot.send_message(message.chat.id, text="_⏳ Downloading video with title '{0}'_".format(video.title), parse_mode="Markdown")
        video.streams.first().download(filename=str(message.chat.id))
        file = open("{}.mp4".format(message.chat.id), 'rb')
        bot.send_video(message.chat.id, file)
        bot.send_message(message.chat.id, text="_🙏 Thanks for using this bot!_", parse_mode="Markdown")
        users_per_hour.append(message.chat.id)
        users_per_day.append(message.chat.id)
        file.close()
        os.remove("{}.mp4".format(message.chat.id))  
    except Exception as e:
        if "regex_search: could not find match for" in str(e):
            bot.send_message(message.chat.id, text="_⛔ Invalid link for video. Make sure you have copied link from YouTube.com_", parse_mode="Markdown")
        elif "Request Entity Too Large" in str(e):
            bot.send_message(message.chat.id, text="_⛔ Размер видеоролика слишком большой(> 50MB). Мы работаем над решением данной проблемы._", parse_mode="Markdown")
            file.close()
            os.remove("{}.mp4".format(message.chat.id))
        else:
            global errors_per_day
            print(str(e))
            bot.send_message(message.chat.id, text="_⛔ There was an error while sending video. Administrarion got report of error._", parse_mode="Markdown")
            errors_per_day.append(str(e))

def create_thread(message):
    Thread(target=get_url, args=(message,)).start()


@bot.message_handler(commands=['start'])
def greetings(message):
    main_buttons_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    get_url_btn = telebot.types.KeyboardButton(text = "Download YouTube Video")
    get_support_btn = telebot.types.KeyboardButton(text = "Support")
    get_info_btn = telebot.types.KeyboardButton(text="About Project")
    main_buttons_markup.add(get_url_btn, get_support_btn, get_info_btn)
    bot.send_message(message.chat.id, text="_🙋 Hi, use command below to download video from YouTube or type to Support😚_", parse_mode="Markdown", reply_markup=main_buttons_markup)


@bot.message_handler(commands=['stats'])
def admin(message):
    global users_per_hour, users_per_day
    if message.chat.id == ADMIN_ID:
        stats_inline_markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
        stats_users_day = telebot.types.InlineKeyboardButton(text = "Stats for day", callback_data = "day_stats")
        stats_users_hour = telebot.types.InlineKeyboardButton(text = "Stats for hour", callback_data = "hour_stats")
        stats_inline_markup.add(stats_users_day, stats_users_hour)
        bot.send_message(ADMIN_ID, text="Choose option to see: ", reply_markup=stats_inline_markup)
    else:
        bot.send_message(message.chat.id, text="⛔ Not enought rights to use this command")


@bot.message_handler(content_types=['text'])
def text_reply(message):
    if message.text == "Download YouTube Video":
        bot.send_message(message.chat.id, text="_🌈 Send link on YouTube video in next message._", parse_mode="Markdown")
        bot.register_next_step_handler(message, create_thread)
    if message.text == "Support":
        bot.send_message(message.chat.id, text="_📞 To connect with support type here: ADMIN_LINK _", parse_mode="Markdown")
    if message.text == "About Project":
        bot.send_message(message.chat.id, text="_📝 This bot written by:_ \n*  ADMIN_LINK* \n_🔧 Modules from project:_ \n*  https://github.com/pytube/pytube*\n*  https://github.com/eternnoir/pyTelegramBotAPI*", parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "day_stats":
        message = "*Today bot have been used by {} people:*\n".format(len(users_per_day))
        for id in users_per_day:
            message += "_{}_\n".format(id)
        bot.send_message(ADMIN_ID, text=message, parse_mode = "Markdown")
    if call.data == "hour_stats":
        message = "*For the last hour bot have been used by {} people:*\n".format(len(users_per_hour))
        for id in users_per_hour:
            message += "_{}_\n".format(id)
        bot.send_message(ADMIN_ID, text=message, parse_mode = "Markdown")


if __name__ == "__main__":
    t1 = Thread(target=count_users)
    t1.start()
    bot.polling()
