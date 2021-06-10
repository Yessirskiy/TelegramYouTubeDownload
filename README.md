# TelegramYouTubeDownload
This bot developed to use in Telegram.
## How to use launched bot?
When you pressed "START" button you see menu of 3 buttons:
1. Download YouTube Video
    After you pressed this button in the next message you should send link to YouTube Video.
    You are gonna get error message if send wrong video.
    *Set messages in **text_reply** function*

2. Support
    Here is a simple one message reply.
    *Set message to reply in **text_reply** function*

3. About Project
    Here is a simple one message reply.
    *Set message to reply in **text_reply** function*

## How do I set my bot?
### To use bot you have to set at least 3 parameters:
1. BOT_TOKEN

    To get this token type to @BotFather.
    Type "/newbot", then follow instructions.
    If you complete all of the instrution well you get BOT_TOKEN in the reply message from BotFather.
    Paste it.

2. ADMIN_ID

    You can get your ADMIN_ID using "get_admin_id.py" file. 
    Paste BOT_TOKEN you got from BotFather and type **/start** command or just press *START* button.
    Paste ADMIN_ID without double or single quotes.

3. ADMIN_LINK

    Go to Telegram and follow:
    Settings -> Edit Profile -> Aim on Username field and press edit button -> Copy link on bottom of box, after "This link opens a chat with you" -> Paste it.

### Change reply messages:
You can change all of the messages by correcting text parameter in bot.send_message() method
To make text look Italic or Bold use Markdown Format.

### Advanced usage:
1. This bot also provides advanced function to analyze statistic:
1. Default command to see statistic is only available for ADMIN. 
    ADMIN_ID is linked with person who paste ID from reply message from *get_admin_id.py*
2. You can see statistic by command */stats*.
    Change this command by changing *"*stats*"* in @bot.message_handler(commands=['stats'])
3. Stats command could shows statistic of last hour or current day.
2. Errors reports
1. Default exceptions are *big size of video* or *invalid link*.
    Bot is automatically send the report about error to user.
2. Other errors
    If there are any other errors the occured in the process bot automatically add them to log file.
    Each day at 0:00(UTC) bot send report(log file) of errors and amount of users.

## How do I get this bot?
#### 1. Make sure you have all the modules installed:
To make this bot works you need few libraries installed:
1. **pytube==10.8.4** . If you don't have this module use command *pip install pytube* to get.
2. **pyTelegramBotAPI==3.7.9** . If you don't have this module use command *pip install pyTelegramBotAPI* to get.

#### 2. Clone Repository
1. Use command *git clone https://github.com/Yessirskiy/TelegramYouTubeDownload.git*.

#### 3. Use command *python main.py* to launch bot.