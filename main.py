import asyncio
import os
import logging

import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from vnstat import vnstat_this_month_usage, human_bytes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


TOKEN = os.environ.get("TOKEN")
LIMIT_GIB = 1024 ** 3 * int(os.environ.get("LIMIT_GIB"))
INTERFACE = os.environ.get("INTERFACE")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")


async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"I'm a bot, please talk to me! Your id: {update.effective_chat.id}"
    )


async def status(update: Update, context: CallbackContext):
    print(update)
    await send_status(update.effective_chat.id)


async def send_status(chat_id):
    interface_name, rx, tx, total, month = vnstat_this_month_usage(interface_name=INTERFACE)
    percent_used = total / LIMIT_GIB * 100
    emoji = '🍏'
    if percent_used > 20: emoji = '✍️'
    if percent_used > 30: emoji = '🧐'
    if percent_used > 40: emoji = '🥴'
    if percent_used > 50: emoji = '👽'
    if percent_used > 60: emoji = '☢️'
    if percent_used > 80: emoji = '❗️'
    if percent_used > 90: emoji = '💥'
    text = f'''Usage on {interface_name} in {month}:
⬇️{human_bytes(rx)}
⬆️{human_bytes(tx)}
Total: {human_bytes(total)}

Limit: {human_bytes(LIMIT_GIB)} ({emoji} {percent_used:.2f}% used)
'''
    await application.bot.send_message(chat_id=chat_id, text=text)


if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('status', status))

    asyncio.get_event_loop().run_until_complete(send_status(chat_id=TG_CHAT_ID))

    # application.run_polling()