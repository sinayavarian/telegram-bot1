import telebot
import os
import pprint
import json
from telebot import apihelper

apihelper.ENABLE_MIDDLEWARE = True

API_TOKEN = os.environ.get("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    #pprint.pprint(message.chat.__dict__,width=4)
    # bot.reply_to(message, """\
# Hi there, I am EchoBot.
# I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
# """)
    bot.send_message(message.chat.id, json.dumps(message.chat.__dict__, indent=4, ensure_ascii=False))



@bot.middleware_handler(update_types=['message'])
def modify_message(bot_instance, message):
    # modifying the message before it reaches any other handler 
    message.another_text = message.text + ':changed'

@bot.message_handler(func = lambda message : True)
def reply_modified(message):
    bot.reply_to(message, message.another_text)

bot.infinity_polling()