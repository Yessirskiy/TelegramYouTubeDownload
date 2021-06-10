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
To use bot you have to set at least 3 parameters:
1. BOT_TOKEN
    To get this token type to @BotFather.
    Type "/newbot", then follow instructions.
    If you complete all of the instrution well you get BOT_TOKEN in the reply message from BotFather.
    Paste it.
2. ADMIN_ID
    You can get your ADMIN_ID using "get_admin_id.py" file. 
    Paste BOT_TOKEN you got from BotFather and type "/start" command or just press "START" button.
    Paste ADMIN_ID without double or single quotes.
3. ADMIN_LINK
    Go to Telegram and follow:
    1. Settings
    2. Edit Profile
    3. Aim on Username field and press edit button
    4. Copy link on bottom of box, after "This link opens a chat with you"
    Paste it.
