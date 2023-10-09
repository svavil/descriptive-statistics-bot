def describe(number_list):
    # returns a textual description of a list of numbers
    import numpy as np
    count = len(number_list)
    if (0 == count):
        return("Чисел нет")
    mean = np.mean(number_list)
    mmin = np.min(number_list)
    mmax = np.max(number_list)
    return "Список из " + str(count) + " чисел со средним " + str(round(mean, 2)) + ", минимумом " + str(round(mmin, 2)) + " и максимумом " + str(round(mmax, 2))

import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Бот запоминает любые присланные числа. Выберите /clear, чтобы их забыть, или /schedule, чтобы отправлять сообщения каждую минуту.")


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    try:
        response = describe(context.chat_data["statistics"])
    except KeyError:
        response = "Бот ещё не запомнил ни одного числа"
    await context.bot.send_message(job.chat_id, text="[Запланированное сообщение] " + response)


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, 60, chat_id=chat_id, name=str(chat_id), data=context.chat_data)

        text = "Через 60 секунд будет прислано сообщение"
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Чтобы запланировать сообщение, пришлите /schedule")


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Запланированное сообщение отменено"
    await update.message.reply_text(text)
    
async def remember(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remembers the number stored in a text message"""
    try: 
        numeric_message = float(update.message.text)
        try:
            context.chat_data.update({"statistics": context.chat_data["statistics"] + [numeric_message]})
        except KeyError:
            context.chat_data.update({"statistics": [numeric_message]})
        reply_text = describe(context.chat_data["statistics"])
    except ValueError:
        reply_text = "Это не число и бот его не запомнит"
    await update.message.reply_text(reply_text)
    
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clears the chat data"""
    context.chat_data.clear()
    await update.message.reply_text("Текущие числа забыты")


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    TOKEN = os.environ["BOT_TOKEN"]
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("schedule", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(MessageHandler(filters.TEXT, remember))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
