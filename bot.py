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


FULLNAME, PHONE, GOODBYE = range(3)
USERNAME = ''
SERVICE = ''
user_data = {}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    global USERNAME
    if len(user.username) == 0:
        USERNAME = user.first_name
    else:
        USERNAME = user.username
    user_data[USERNAME] = {}
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
    """

    await update.message.reply_text(text,
        reply_markup=reply_markup
    )
    return FULLNAME

async def get_fullname(update:Update, context:ContextTypes.DEFAULT_TYPE):
    selected_button = update.callback_query.data
    global SERVICE
    SERVICE = selected_button
    selected_button_m = update.callback_query.message.reply_markup.inline_keyboard
    logger.info('Button %s selected by %s', selected_button, USERNAME)
    if selected_button == 'laser':
        message = selected_button_m[0][0].text
        await update.callback_query.message.reply_text("""  🎉 قراره برای همیشه از موهای زائد خلاص بشید؛
ما در دیواژ از بهترین دستگاه های لیزر در جهان استفاده میکنیم

صد درصد تضمینی و بدون درد  💚😌

مشاورین ما توضیحات کامل تری به شما خواهند داد. برای (مشاوره رایگان) و دریافت تخفیف ویژه دیواژ، لطفا «نام و نام خانوادگی» خود را وارد کنید.""")
    elif selected_button == 'thinness':
        message = selected_button_m[0][1].text
        await update.callback_query.message.reply_text("""عالیــه، خودتون رو برای یک استایل جدید آماده کنید 😌
در دیواژ با بهترین دستگاه ها و خدمات لاغری بدن و صورت در خدمت شما هستیم. (حتی برای سلولیت!) ✨

مشاورین ما توضیحات کامل تری به شما خواهند داد. برای (مشاوره رایگان) و دریافت تخفیف ویژه دیواژ، لطفا «نام و نام خانوادگی» خود را وارد کنید.""")
    elif selected_button == 'botox':
        message = selected_button_m[1][0].text
        await update.callback_query.message.reply_text("""جذابیت انتها نداره😌
در دیواژ با خدمات مختلف فرم دهی بدون جراحی و با جراحی، تزریقات ژل و فیلر، PRP  و لیفت صورت در خدمتتون هستیم.  

 مشاورین ما توضیحات کامل تری به شما خواهند داد. برای (مشاوره رایگان) و دریافت تخفیف ویژه دیواژ، لطفا «نام و نام خانوادگی» خود را وارد کنید.
""")
    else:
        message = selected_button_m[1][1].text
        await update.callback_query.message.reply_text("""زیبـــاتر از همیشــه خواهید بود🤍
ما برای رفع خط خنده، چروک های پوستی، خال‌برداری و هر موضوع دیگه ای، بهترین راهکار‌‌ ها رو براتون در نظر گرفتیم.  

مشاورین ما توضیحات کامل تری به شما خواهند داد. برای (مشاوره رایگان) و دریافت تخفیف ویژه دیواژ، لطفا «نام و نام خانوادگی» خود را وارد کنید.
""")
    user_data[USERNAME]['نوع خدمت'] = message
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    fullname = update.message.text
    logger.info("%s is the fullname of %s", fullname, USERNAME)
    user_data[USERNAME]['نام و نام خانوادگی'] = fullname
    await update.message.reply_text("""مشتاق شنیدن صدای شما هستیم. 
لطفاً شماره تماس خود را وارد کنید  ☎️""")
    return GOODBYE

async def goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    phone = update.message.text
    logger.info("%s sent his/her phone: %s", USERNAME, phone)
    if SERVICE == 'laser' or SERVICE == 'thinness':
        await update.message.reply_text("""ضمن تشکر از همراهی شما، (کد تخفیف ۱۵٪) روی شماره شما اعمال شد. مشاورین ما به زودی با شما تماس خواهند گرفت ✨⏳

    🚘  اگر خودروی شخصی دارید، نگران جای پارک نباشید. ما براتون پارکینگ و محل پارک در نظر گرفتیم.
    ☕  ضمن اینکه یک قهوه یا دمنوش در کافه کلینیک دیواژ میهمان ماهستید.

    •  •  •  بــه زودی میبینیـمتـــــــون 😍👌🏻""")
    else:
            await update.message.reply_text("""ضمن تشکر از همراهی شما، (کد تخفیف ۱۰٪) روی شماره شما اعمال شد. مشاورین ما به زودی با شما تماس خواهند گرفت ✨⏳

 🚘  اگر خودروی شخصی دارید، نگران جای پارک نباشید. ما براتون پارکینگ و محل پارک در نظر گرفتیم.
 ☕️  ضمن اینکه یک قهوه یا دمنوش در کافه کلینیک دیواژ میهمان ماهستید.

•  •  •  بــه زودی میبینیـمتـــــــون 😍""")
    try:
        df = pd.read_excel('user_data.xlsx')
        new_df = pd.DataFrame(user_data[USERNAME], index=[0])
        df = pd.concat([df, new_df], ignore_index=False)
        df.to_excel('user_data.xlsx', index=False)
        user_data.clear()
    except:
        df = pd.DataFrame(user_data[USERNAME], index=[0])
        df.to_excel('user_data.xlsx', index=False)

    await context.bot.send_document(chat_id=-1001618112364, document='user_data.xlsx')
    logger.info('bye')
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token('5849241070:AAEdawgN0e0Pa8NUsNpwwJpcsxgtuIhD4Ss').build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FULLNAME: [CallbackQueryHandler(get_fullname, pattern='^(laser|thinness|botox|skin)$')],
            PHONE: [MessageHandler(filters.TEXT, get_phone)],
            GOODBYE: [MessageHandler(filters.TEXT, goodbye)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()