from pytube import YouTube
import telebot
import os
from threading import Thread
import time


BOT_TOKEN = '' # Your Bot Token Here
ADMIN_ID = 0 # Your Admin Id Here
ADMIN_LINK = "https://t.me/dobrydnevk" # Link On Your Telegram Profile
bot = telebot.TeleBot(BOT_TOKEN)
users_per_day = []
users_per_hour = []
errors_per_day = []
day_count = time.strftime("%d")
hour_count = time.strftime("%H")
users_info = {}

def resolution_buttons(resolutions, message): # Resolution buttons
    users_info[message.chat.id] = telebot.types.InlineKeyboardMarkup(row_width = 1)
    for resolution in resolutions:
        if resolution <= 1440:
            users_info[message.chat.id].add(telebot.types.InlineKeyboardButton(text = str(resolution) + "p", callback_data = str(resolution)))
    return users_info[message.chat.id]

def count_users(): # Counting users
    global day_count, hour_count, users_per_hour, users_per_day, errors_per_day
    while True:
        if day_count != time.strftime("%d"):
            file = open(time.strftime("%d-%m-%Y-log.txt"), 'w')
            file.write("Today bot have been used by {0} people.\n Errors today {1}:\n".format(len(users_per_day), len(errors_per_day)))
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
        users_info[message.chat.id] = set()
        url = message.text
        video = YouTube(url)
        for i in video.streams:
            if i.resolution != None and 'mp4a.40.2' or 'mp4v.20.3' in i.codecs:
                users_info[message.chat.id].add(int(str(i.resolution).replace("p", "")))
        users_info[message.chat.id] = sorted(users_info[message.chat.id])
        bot.send_message(message.chat.id, text = "_Choose resolution:_", reply_markup = resolution_buttons(users_info[message.chat.id], message), parse_mode="Markdown")
        while True:
            if type(users_info[message.chat.id]) == str:
                if video.streams.filter(res=users_info[message.chat.id]).first().filesize < 50000000:
                    bot.send_message(message.chat.id, text="_⏳ Downloading video. Title is '{0}'. Video quality is {1}_".format(video.title, users_info[message.chat.id]), parse_mode="Markdown")
                    video.streams.filter(res=users_info[message.chat.id], file_extension='mp4').first().download(filename=str(message.chat.id))
                    file = open("{}".format(message.chat.id), 'rb')
                    bot.send_video(message.chat.id, file)
                    bot.send_message(message.chat.id, text="_🙏 Thanks for using this bot!_", parse_mode="Markdown")
                    users_per_hour.append(message.chat.id)
                    users_per_day.append(message.chat.id)
                    file.close()
                    os.remove("{}".format(message.chat.id))
                else:
                    bot.send_message(message.chat.id, text="_⛔ Size of video is too large(> 50MB). We are currently working on this problem._", parse_mode="Markdown")
                del users_info[message.chat.id]    
                break
    except Exception as e:
        if "regex_search: could not find match for" in str(e):
            bot.send_message(message.chat.id, text="_⛔ Incorrect link on video. Make sure you send link on video from YouTube.com_", parse_mode="Markdown")
            del users_info[message.chat.id]
        else:
            global errors_per_day
            print(str(e))
            bot.send_message(message.chat.id, text="_⛔ Error occured while sending video. Administration have already got report._", parse_mode="Markdown")
            errors_per_day.append(str(e))
            del users_info[message.chat.id]

def create_thread(message):
    Thread(target=get_url, args=(message,)).start()
    

@bot.message_handler(commands=['start'])
def greetings(message):
    main_buttons_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    get_url_btn = telebot.types.KeyboardButton(text = "Download YouTube video")
    get_support_btn = telebot.types.KeyboardButton(text = "Support")
    get_info_btn = telebot.types.KeyboardButton(text="About Project")
    main_buttons_markup.add(get_url_btn, get_support_btn, get_info_btn)
    bot.send_message(message.chat.id, text="_🙋 Hey, use button in menu below to donwload video from YouTube or to text to support😚_", parse_mode="Markdown", reply_markup=main_buttons_markup)


@bot.message_handler(commands=['stats'])
def admin(message): # Admin functions
    global users_per_hour, users_per_day
    if message.chat.id == ADMIN_ID:
        stats_inline_markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
        stats_users_day = telebot.types.InlineKeyboardButton(text = "Daily stats", callback_data = "day_stats")
        stats_users_hour = telebot.types.InlineKeyboardButton(text = "Last hour stats", callback_data = "hour_stats")
        stats_inline_markup.add(stats_users_day, stats_users_hour)
        bot.send_message(ADMIN_ID, text="Choose option to show:", reply_markup=stats_inline_markup)
    else:
        bot.send_message(message.chat.id, text="⛔ No rights to call this command.")


@bot.message_handler(content_types=['text'])
def text_reply(message):
    if message.text == "Скачать Видео YouTube":
        bot.send_message(message.chat.id, text="_🌈 Send YouTube video link in the next message._", parse_mode="Markdown")
        bot.register_next_step_handler(message, create_thread)
    if message.text == "Поддержка":
        bot.send_message(message.chat.id, text="_📞 Text here to contact with support: {} _".format(ADMIN_LINK), parse_mode="Markdown")
    if message.text == "О Проекте":
        bot.send_message(message.chat.id, text="_📝 Данный бот написан:_ \n * {} * \n_🔧 Modules from project:_ \n*  https://github.com/pytube/pytube*\n*  https://github.com/eternnoir/pyTelegramBotAPI*".format(ADMIN_LINK), parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "day_stats":
        message = "*Today bot has been used by {} people.*\n".format(len(users_per_day))
        for id in users_per_day:
            message += "_{}_\n".format(id)
        bot.send_message(ADMIN_ID, text=message, parse_mode = "Markdown")
    if call.data == "hour_stats":
        message = "*Last hour bot has been used by {} people.*\n".format(len(users_per_hour))
        for id in users_per_hour:
            message += "_{}_\n".format(id)
        bot.send_message(ADMIN_ID, text=message, parse_mode = "Markdown")
    if (int(call.data)%120 == 0 and int(call.data)/120 <= 12) or call.data == "144":
        users_info[call.message.chat.id] = call.data + "p"


if __name__ == "__main__":
    t1 = Thread(target=count_users)
    t1.start()
    bot.polling()
