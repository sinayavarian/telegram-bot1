import telebot
import os
import pprint
import json
from telebot import apihelper
import logging
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
# Dictionary to store user profiles
user_profiles = {}

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

apihelper.ENABLE_MIDDLEWARE = True

API_TOKEN = os.environ.get("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help'])
def send_welcome(message):
    logger.info("Triggered welcome")
    #pprint.pprint(message.chat.__dict__,width=4)
    # bot.reply_to(message, """\
# Hi there, I am EchoBot.
# I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
# """)
    bot.send_message(message.chat.id, json.dumps(message.chat.__dict__, indent=4, ensure_ascii=False))

@bot.message_handler(commands=['dorood'])
def send_welcome(message):
    bot.send_message(message.chat.id, """Dorood""")
@bot.message_handler(commands=['author'])
def send_author(message):
    bot.send_message(message.chat.id, """the author is Sina Yavarian""")

# @bot.middleware_handler(update_types=['message'])
# def modify_message(bot_instance, message):
#     # modifying the message before it reaches any other handler 
#     message.another_text = message.text + ':changed'

# @bot.message_handler(func = lambda message : True)
# def reply_modified(message):
#     bot.reply_to(message, message.another_text)


# Step 1: Start command handler
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.reply_to(message, "سلام! لطفاً نام خود را وارد کنید:")
#     bot.register_next_step_handler(message, ask_name)

# # Step 2: Function to ask for name
# def ask_name(message):
#     chat_id = message.chat.id
#     name = message.text
#     user_profiles[chat_id] = {'name': name}
#     bot.reply_to(message, f"خوش آمدید {name}! لطفاً سن خود را وارد کنید:")
#     bot.register_next_step_handler(message, ask_age)

# # Step 3: Function to ask for age
# def ask_age(message):
#     chat_id = message.chat.id
#     age = message.text
#     user_profiles[chat_id]['age'] = age
#     bot.reply_to(message, f"اطلاعات شما ثبت شد:\nنام: {user_profiles[chat_id]['name']}\nسن: {age}")


# @bot.message_handler(commands=['start'])
# def create_button(message):

#     markup = ReplyKeyboardMarkup(resize_keyboard=True,input_field_placeholder="choose your option")
#     markup.add(KeyboardButton('Help'),KeyboardButton('About'))
    
#     # display this markup:
 
#     bot.send_message(message.chat.id, """Hi! Welcome!""", reply_markup=markup)

# @bot.message_handler(func= lambda message : message.text == "Help")
# def send_help(message):
#     bot.send_message(message.chat.id, "It is your Help you want!")

# @bot.message_handler(func= lambda message : message.text == "About")
# def send_about(message):
#     bot.send_message(message.chat.id, "It is your About you want!")

@bot.message_handler(commands=['start'])
def create_inline_button(message):

    markup = InlineKeyboardMarkup()
    google_button =InlineKeyboardButton("google",url="https://google.com")
    mysite_button =InlineKeyboardButton("My site",url="https://yavarian.com")
    step2_button = InlineKeyboardButton("step2", callback_data="step2")
    markup.add(google_button,mysite_button)
    markup.add(step2_button)
    # display this markup:
 
    bot.send_message(message.chat.id, """Hi! Welcome!""",reply_markup=markup)

@bot.callback_query_handler(func= lambda call:True)
def reply_call(call):
    #logger.debug(call.__dict__)
    if call.data =="step2":
        markup = InlineKeyboardMarkup()
        step3_button = InlineKeyboardButton("step3", callback_data="step3")
        cancel_button = InlineKeyboardButton("cancel", callback_data="cancel")
        markup.add(step3_button,cancel_button)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text="choose your next step" ,reply_markup=markup)
       # bot.answer_callback_query(call.id, "click on test",show_alert=True)
    if call.data == "step3":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text="your reference code is 1312" )
       # bot.send_message(call.message.chat.id,"Done")
    if call.data == "cancel":
        bot.answer_callback_query(call.id, "the mission has been canceled", show_alert=True)
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.id,timeout=5)

@bot.message_handler(commands=['send_photo'])
def send_photo(message):
    #photo = open('./test/file/test.jpg', 'rb')
    bot.send_chat_action(message.chat.id, action="upload_photo")
    bot.send_photo(message.chat.id, "AgACAgQAAxkBAAOJZ0PjkTSelcko50mEM-u-JFOG384AAnjHMRuCriBSR-KX17Fv4PcBAAMCAAN4AAM2BA")

@bot.message_handler(content_types=["document", "video","photo","voice","audio"])
def get_id(message)    :
    logger.info(message.__dict__)

# @bot.message_handler(func= lambda message : message.text == "Help")
# def send_help(message):
#     bot.send_message(message.chat.id, "It is your Help you want!")

# @bot.message_handler(func= lambda message : message.text == "About")
# def send_about(message):
#     bot.send_message(message.chat.id, "It is your About you want!")

bot.infinity_polling()