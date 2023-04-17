import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
import requests

headers = {
    "X-RapidAPI-Key": "871aadb731msh302174792d744b8p1b59bdjsn482167023d41",
    "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
reply_keyboard = [['/start', '/help'],
                  ['/info_country', '/game_capital', '/game_flag']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
contr = ""
count = 0
cor = 0


def get_response(countru):
    url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/countries/US"  # бд
    response = requests.request("GET", url, headers=headers)
    return response.json()


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
    await update.message.reply_text(
        "Привет. Я готов рассказать тебе о любой стране, которую знаю. Пожалуйста напиши название страны!")
    return 1


async def game_capital(update, context):
    await update.message.reply_text(
        "Привет! И так начнем игру")
    info = get_response('us')  # Рандом и бд
    await update.message.reply_text(
        f"{info['data']['capital']}\n")
    global count, cor
    count = 0
    cor = 0
    return 1


async def game_flag(update, context):
    await update.message.reply_text(update.message.text)


async def first_response_info(update, context):
    locality = update.message.text  # Лезем в бд получаем id страны и создаем запрос. из запроса берем информацию и загружаем картинку. Здесь лежит страна
    info = get_response(locality)
    await update.message.reply_text(
        f"Полное название страны {info['data']['name']}\n"
        f"Столица {info['data']['capital']}\n")
    await update.message.reply_text("Хотите вы продолжить?")
    return 2


async def second_response_info(update, context):
    locality = update.message.text
    if locality == 'да':
        await update.message.reply_text("Напишите новую страну")
        return 1
    else:
        await update.message.reply_text("Всего доброго!")
        return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def first_response_capital(update, context):
    locality = update.message.text
    info = get_response('us')
    global count, cor
    if locality == info['data']['name']:
        await update.message.reply_text('Верно')
        cor += 1
    else:
        await update.message.reply_text("Неверно")
        count += 1
    if count < 2:
        return 2
    await update.message.reply_text(f'Вы проиграли вас результат {cor}')
    return ConversationHandler.END


async def second_response_capital(update, context):
    info = get_response('us')  # Рандом и бд
    await update.message.reply_text(
        f"{info['data']['capital']}\n")
    locality = update.message.text
    global count, cor
    if locality == info['data']['name']:
        await update.message.reply_text('Верно')
        cor += 1
    else:
        await update.message.reply_text("Неверно")
        count += 1
    if count < 2:
        return 1
    await update.message.reply_text(f'Вы проиграли вас результат {cor}')
    return ConversationHandler.END


info_handler = ConversationHandler(
    entry_points=[CommandHandler('info_country', info_country)],
    states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response_info)],
        2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response_info)]
    },
    fallbacks=[CommandHandler('stop', stop)]
)
capital_handler = ConversationHandler(
    entry_points=[CommandHandler('game_capital', game_capital)],
    states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response_capital)],
        2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response_capital)]
    },
    fallbacks=[CommandHandler('stop', stop)]
)


def main():
    application = Application.builder().token("6211811458:AAE10kS4o9HfzHTQa_uGXHaWXuqu2bia83A").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("game_flag", game_flag))
    application.add_handler(info_handler)
    application.add_handler(capital_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
