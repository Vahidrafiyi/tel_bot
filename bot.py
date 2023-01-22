#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import __version__ as TG_VER
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)
import pandas as pd


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
fh = logging.FileHandler('bot.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.addHandler(fh)
fh.setFormatter(formatter)
CONSULT, FULL_NAME, EYELID, PHONE, END = range(5)

user_data = {}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_data[user.username] = {}
    logger.info('%s started the bot.', user.username)
    consult_button = InlineKeyboardButton('مشاوره رایگان با متخصص', callback_data='consult')
    keyboard = [[consult_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text =f"""
    ✅ سلام {user.first_name} عزیز

🔺 برای مشاوره تخصصی و رایگان جراحی افتادگی پلک توسط فوق تخصص جراحی پلاستیک بدون استفاده از تیغ با برش لیزری لازم است تا چند سوال کوتاه را پاسخ دهيد.

💰  تخفیف ویژه

💎 مشاوره تخصصی رفع افتادگی پلک بالا و پف پلک پایین توسط متخصص جراحی پلاستیک

📣 پیشنهاد ویژه : برای مشاوره رایگان  با متخصصان و ثبت نام در لیست تخفیف ویژه به مدت محدود کلید زیر را فشار دهید 👇👇👇
    """

    await update.message.reply_text(text,
        reply_markup=reply_markup
    )
    return CONSULT

async def button_hanlder(update:Update, context:ContextTypes.DEFAULT_TYPE):
    selected_button = update.callback_query.data
    user = update.callback_query.from_user
    logger.info('Button %s selected by %s', selected_button, user.username)
    await update.callback_query.message.reply_text('لطفا شهر محل سکونت خود را وارد کنید.👇')
    return FULL_NAME

async def full_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    city = update.message.text
    logger.info("%s is the city of %s", city, user.username)
    user_data[user.username]['شهر'] = city
    await update.message.reply_text('لطفا نام و نام خانوادگی خود را وارد نمایید.👇👇👇')
    return EYELID


async def eyelid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info('fullname of %s : %s', user.username, update.message.text)
    user_data[user.username]['نام و نام خانوادگی'] = update.message.text
    eyelid_left= InlineKeyboardButton('پلک چپ', callback_data='left')
    eyelid_right= InlineKeyboardButton('پلک راست', callback_data='right')
    keyboard = [[eyelid_left, eyelid_right]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'کدام پلک خود را تمایل دارید جراحی کنید؟👇👇👇.',
        reply_markup=reply_markup
    )

    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user
    logger.info("%s selected %s eyelid",user.username, update.callback_query.data)
    eye = ''
    if update.callback_query.data == 'right':
        eye = 'راست'
    else:
        eye = 'چپ'
    user_data[user.username]['پلک'] = eye
    await update.callback_query.message.reply_text('برای مشاوره رایگان با متخصصان و ثبت نام در لیست  تخفیف ویژه شماره تماس خود را وارد کنید. 👇👇👇')
    return END


async def good_bye(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s phone : %s", user.first_name, update.message.text)
    user_data[user.username]['موبایل'] = update.message.text
    text = f"""🙏🏻تشکر {user.first_name} گرامی؛
✅ درخواست شما با موفقیت در سامانه کیلینیک الهام ثبت گردید.

☎️ متخصصین برای مشاوره رایگان و تعیین وقت با شما تماس خواهند گرفت."""
    await update.message.reply_text(text)
    df = pd.read_excel('user_data.xlsx')

    # Write the DataFrame back to the Excel file
    new_df = pd.DataFrame(user_data[user.username], index=[0])
    df = pd.concat([df, new_df], ignore_index=False)
    df.to_excel('user_data.xlsx', index=False)
    user_data.clear()
    await context.bot.send_document(chat_id=-852229182, document='user_data.xlsx')
    return ConversationHandler.END



def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token('5974728163:AAEE3v19L7GpiGC1WX4O5lpPY-XRo8vxg9g').build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CONSULT: [CallbackQueryHandler(button_hanlder, pattern='^consult$')],
            FULL_NAME: [MessageHandler(filters.TEXT, full_name)],
            EYELID: [MessageHandler(filters.TEXT, eyelid)],
            PHONE: [CallbackQueryHandler(get_phone, pattern='^(left|right)$')],
            END: [MessageHandler(filters.TEXT, good_bye)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()