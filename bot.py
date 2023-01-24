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
from logging_module import logger


CONSULT, FULL_NAME, EYELID, PHONE, END = range(5)
USERNAME = ''
user_data = {}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    global USERNAME
    if len(user.username) == 0:
        USERNAME = user.first_name
    else:
        USERNAME = user.username
    user_data[USERNAME] = {}
    print(USERNAME)
    print(user_data[USERNAME])
    logger.info('%s started the bot.', USERNAME)
    laser = InlineKeyboardButton('لیزر و رفع موهای زائد', callback_data='laser')
    thinness = InlineKeyboardButton('لاغری تضمینی', callback_data='thinness')
    botox = InlineKeyboardButton('فرم‌دهی صورت، فیلر و بوتاکس', callback_data='botox')
    skin = InlineKeyboardButton('جوان سازی و شادابی پوست', callback_data='skin')
    keyboard = [[laser, thinness],[botox, skin]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text =f"""
    {USERNAME} عزیز 👋🏻

| متخصصیـن ما در دیواژ  با بیش از چهل خدمت متنوع در کنار شما هستند، لطفاً دسته بندی مورد نظرتان را انتخاب نمایید 🌟

لیست کلید خدمات:
1️⃣ لیزر و رفع موهای زائد
2️⃣ لاغری تضمینی
3️⃣ فرم‌دهی صورت، فیلر و بوتاکس
4️⃣ جوان سازی و شادابی پوست
    """

    await update.message.reply_text(text,
        reply_markup=reply_markup
    )
    return CONSULT

async def button_hanlder(update:Update, context:ContextTypes.DEFAULT_TYPE):
    print(f'username: {USERNAME}')
    selected_button = update.callback_query.data
    selected_button_m = update.callback_query.message
    print(selected_button_m)
    logger.info('Button %s selected by %s', selected_button, USERNAME)
    user_data[USERNAME]['نوع خدمت'] = selected_button
    if selected_button == 'laser':
        await update.callback_query.message.reply_text(""" 🎉 قراره برای همیشه از موهای زائد خلاص بشید؛
ما در دیواژ از بهترین دستگاه های لیزر در جهان استفاده میکنیم

صد درصد تضمینی و بدون درد  💚😌

مشاورین ما توضیحات کامل تری به شما خواهند داد. برای (مشاوره رایگان) و دریافت تخفیف ویژه دیواژ، لطفا «نام و نام خانوادگی» خود را وارد کنید.""")
    elif selected_button == 'thinness':
        await update.callback_query.message.reply_text("""عالیــه، خودتان را برای یک استایل جدید آماده کنید 😌
در دیواژ با بهترین دستگاه ها و خدمات لاغری بدن و صورت در خدمت شما هستیم. (حتی برای سلولیت!) ✨

مشاورین ما توضیحات کامل تری به شما خواهند داد. برای (مشاوره رایگان) و دریافت تخفیف ویژه دیواژ، لطفا «نام و نام خانوادگی» خود را وارد کنید.
""")
    elif selected_button == 'botox':
        await update.callback_query.message.reply_text("""جذابیت انتها نداره😌
در دیواژ با خدمات مختلف فرم دهی بدون جراحی و با جراحی، تزریقات ژل و فیلر، PRP  و لیفت صورت در خدمتتون هستیم.  

 مشاورین ما توضیحات کامل تری به شما خواهند داد. برای (مشاوره رایگان) و دریافت تخفیف ویژه دیواژ، لطفا «نام و نام خانوادگی» خود را وارد کنید.
""")
    else:
        await update.callback_query.message.reply_text("""زیبـــاتر از همیشــه خواهید بود🤍
ما برای رفع خط خنده، چروک های پوستی، خال‌برداری و هر موضوع دیگه ای، بهترین راهکار‌‌ ها رو براتون در نظر گرفتیم.  

مشاورین ما توضیحات کامل تری به شما خواهند داد. برای (مشاوره رایگان) و دریافت تخفیف ویژه دیواژ، لطفا «نام و نام خانوادگی» خود را وارد کنید.
""")
    return FULL_NAME

async def full_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    fullname = update.message.text
    logger.info("%s is the fullname of %s", fullname, USERNAME)
    user_data[USERNAME]['نام و نام خانوادگی'] = fullname
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
    try:
        df = pd.read_excel('user_data.xlsx')
        new_df = pd.DataFrame(user_data[user.username], index=[0])
        df = pd.concat([df, new_df], ignore_index=False)
        df.to_excel('user_data.xlsx', index=False)
        user_data.clear()
    except:
        df = pd.DataFrame(user_data[user.username], index=[0])
        df.to_excel('user_data.xlsx', index=False)

    await context.bot.send_document(chat_id=-1001618112364, document='user_data.xlsx')
    return ConversationHandler.END



def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token('5849241070:AAEdawgN0e0Pa8NUsNpwwJpcsxgtuIhD4Ss').build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CONSULT: [CallbackQueryHandler(button_hanlder, pattern='^(laser|thinness|botox|skin)$')],
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