from time import sleep
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def describe(number_list):
    # returns a textual description of a list of numbers
    import numpy as np
    count = len(number_list)
    if (0 == count):
        return("No numbers in list")
    mean = np.mean(number_list)
    std = np.std(number_list)
    return "A list of " + str(count) + " samples with mean " + str(round(mean, 2)) + " and deviation " + str(round(std, 2))

def respond_to_message(update, context):
    # Check what kind of message we received
    if ((update.message.text == "/start") or (update.message.text == "/help")):
        reply_text = "Enter numbers to accumulate statistics, or /clear to start from an empty array"
    elif (update.message.text == "/clear"):
        context.chat_data.clear()
        reply_text = "Array cleared"
    else:
        try: 
            numeric_message = float(update.message.text)
            try:
                context.chat_data.update({"statistics": context.chat_data["statistics"] + [numeric_message]})
            except KeyError:
                context.chat_data.update({"statistics": [numeric_message]})
        except ValueError:
            reply_text = "This was not a number. Enter numbers to accumulate statistics"
        reply_text = describe(context.chat_data["statistics"])
    update.message.reply_text(reply_text)

def respond_to_message_template(update, context):
    if ((update.message.text == "/start") or (update.message.text == "/help")):
        reply_text = "О каком вопросе вы сейчас думаете?"
    else:
        reply_text = "Пока я не знаю, что вам ответить"
        ### Здесь должен быть код, который пользуется переменными update.message.text и context.chat_data
        ### и формирует переменную reply_text
    update.message.reply_text(reply_text)

if "__main__" == __name__:
    TOKEN = os.environ["BOT_TOKEN"]
    updater = Updater(TOKEN, use_context = True)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, respond_to_message))
    updater.start_polling()
    print("Telegram bot backbone, polling started...")
    updater.idle()
    
