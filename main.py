import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup
import requests

url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries/RU"
headers = {
    "X-RapidAPI-Key": "871aadb731msh302174792d744b8p1b59bdjsn482167023d41",
    "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
}
response = requests.request("GET", url, headers=headers)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
reply_keyboard = [['/start', '/help'],
                  ['/info_country', '/game_capital', '/game_flag']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот, который поможет тебе подтянуть свои знания по географии и хорошо"
        rf" провести время)", reply_markup=markup
    )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Напишем всякой фигни")  # TO Do: написать что-то


async def info_country(update, context):
    await update.message.reply_text(response.json()['data']['capital']) # КАКАЯ-ТО ХРЕНЬ СДЕЛАЮ ПОТОМ


async def game_capital(update, context):
    await update.message.reply_text(update.message.text)


async def game_flag(update, context):
    await update.message.reply_text(update.message.text)


def main():
    application = Application.builder().token("6211811458:AAE10kS4o9HfzHTQa_uGXHaWXuqu2bia83A").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info_country", info_country))
    application.add_handler(CommandHandler("game_capital", game_capital))
    application.add_handler(CommandHandler("game_flag", game_flag))
    application.run_polling()


if __name__ == '__main__':
    main()
