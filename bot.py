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

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CONSULT, FULL_NAME, EYELID, PHONE, END = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    user = update.message.from_user
    print(user.first_name)
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
    await update.callback_query.message.reply_text('لطفا شهر محل سکونت خود را وارد کنید.👇')
    return FULL_NAME

async def full_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("fullname of %s", user.first_name)
    await update.message.reply_text('لطفا نام و نام خانوادگی خود را وارد نمایید.👇👇👇')
    await context.bot.send_message(chat_id=-852229182, text=update.message.text)
    return EYELID


async def eyelid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    eyelid_left= InlineKeyboardButton('پلک چپ', callback_data='left')
    eyelid_right= InlineKeyboardButton('پلک راست', callback_data='right')
    keyboard = [[eyelid_left, eyelid_right]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'کدام پلک خود را تمایل دارید جراحی کنید؟👇👇👇.',
        reply_markup=reply_markup
    )
    logger.info("the eylid is: %s", update.message.text)
    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    await update.callback_query.message.reply_text('برای مشاوره رایگان با متخصصان و ثبت نام در لیست  تخفیف ویژه شماره تماس خود را وارد کنید. 👇👇👇')
    return END


async def good_bye(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    text = f"""🙏🏻تشکر {user.first_name} گرامی؛

✅ درخواست شما با موفقیت در سامانه کیلینیک الهام ثبت گردید.

☎️ متخصصین برای مشاوره رایگان و تعیین وقت با شما تماس خواهند گرفت."""
    await update.message.reply_text(text)
    return ConversationHandler.END



def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token('5974728163:AAEE3v19L7GpiGC1WX4O5lpPY-XRo8vxg9g').build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CONSULT: [CallbackQueryHandler(button_hanlder)],
            FULL_NAME: [MessageHandler(filters.TEXT, full_name)],
            EYELID: [MessageHandler(filters.TEXT, eyelid)],
            PHONE: [CallbackQueryHandler(get_phone)],
            END: [MessageHandler(filters.TEXT, good_bye)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button_hanlder, pattern='^consult$'))
    application.add_handler(CallbackQueryHandler(get_phone, pattern='^(left|right)$'))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()