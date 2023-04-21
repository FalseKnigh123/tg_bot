import logging
import aiohttp as aiohttp
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from random import choice
from data import db_session
from data.countries import Country
from main2 import create_table
from data.resault import User

db_session.global_init("db/blogs.db")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
reply_keyboard = [['/results', '/info_country'],
                  ['/game_capital', '/game_flag', '/game_location']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
contr = ""
count = 0
cor = 0
info = {}


def update_info():
    global info
    db_sess = db_session.create_session()
    con = db_sess.query(Country).all()
    info = choice(con)


def get_country(country):
    global info
    db_sess = db_session.create_session()
    con = db_sess.query(Country).filter((Country.name == country) | (Country.fullname == country) |
                                        (Country.english == country))[0]
    return con


async def res(update, context):
    user = update.effective_user.mention_html()
    db_sess = db_session.create_session()
    con = db_sess.query(User).filter(User.user_name == user)
    text = ''
    for u in con:
        text += f'Ваш результат в тесте {u.type_game} = {u.score} \n'
    await update.message.reply_text(text)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я - бот, который поможет тебе подтянуть свои знания по географии и хорошо"
        rf" провести время.)", reply_markup=markup
    )


async def help_command(update, context):
    await update.message.reply_text(""
                                    "Команда /start выводит приветствие.\n"
                                    "Команда /help помогает разобрать в использовании бота.\n"
                                    "Команда /results помогает разобрать в использовании бота.\n"
                                    "Команда /info_country позволяет узнать базовые сведения о стране по её названию.\n"
                                    "Команда /game_capital запускает интеллектуальную игру по проверке "
                                    "знания столиц стран.\n"
                                    "Команда /game_flag запускает интеллектуальную игру по проверке знания "
                                    "флагов стран.\n"
                                    "Команда /game_location запускает интеллектуальную игру по проверке знания "
                                    "местоположения стран.\n"
                                    )


async def info_country(update, context):
    await update.message.reply_text(
        "Привет. Я готов рассказать тебе о любой стране, которую знаю. Пожалуйста, напиши название страны!")
    return 1


async def game_capital(update, context):
    global info
    await update.message.reply_text("Привет! И так начнем игру.")
    update_info()
    await update.message.reply_text(
        f"{info.capital}\n")
    global count, cor
    count = 0
    cor = 0
    return 1


async def game_flag(update, context):
    global info
    await update.message.reply_text("Привет! И так начнём игру.")
    update_info()
    await get_image(update, context)
    global count, cor
    count = 0
    cor = 0
    return 1


async def game_location(update, context):
    global info
    await update.message.reply_text("Привет! И так начнём игру.")
    update_info()
    await update.message.reply_text(
        f"{info.name}\n")
    global count, cor
    count = 0
    cor = 0
    return 1


async def first_response_info(update, context):
    global info
    locality = update.message.text
    info = get_country(locality)
    if not info:
        await update.message.reply_text('Такой страны не существует или ты ввел не корректное название')
    else:
        await update.message.reply_text(
            f"Название страны: {info.name}\n"
            f"Полное название страны: {info.fullname}\n"
            f"Столица: {info.capital}\n"
            f"Расположение: {info.location}\n"
            f"Площадь: {info.square}\n"
            f"Язык: {info.language}\n"
            f"Население: {info.population}\n"
            f"Валюта: {info.currentcy}\n")
        await get_image(update, context)
    await update.message.reply_text("Вы хотите продолжить?")
    return 2


async def second_response_info(update, context):
    locality = update.message.text
    if locality.lower() == 'да':
        await update.message.reply_text("Напишите новую страну.")
        return 1
    else:
        await update.message.reply_text("Всего доброго!")
        return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def first_response_capital(update, context):
    locality = update.message.text.title()
    global count, cor
    db_sess = db_session.create_session()
    con = db_sess.query(Country).filter((Country.name == locality) | (Country.fullname == locality) |
                                        (Country.english == locality))
    if list(con):
        await update.message.reply_text('Верно.')
        cor += 1
    else:
        await update.message.reply_text("Неверно.")
        count += 1
    if count < 2:
        await update.message.reply_text("Хотели бы вы подробнее узнать о стране?")
        return 2
    await update.message.reply_text(f'Вы проиграли, Ваш результат: {cor}.')
    user = User()
    user.user_name = update.effective_user.mention_html()
    user.type_game = "Столицы."
    user.score = cor
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    return ConversationHandler.END


async def second_response_capital(update, context):
    locality = update.message.text
    if locality.lower() == 'да':
        await update.message.reply_text(
            f"Название страны: {info.name}\n"
            f"Полное название страны: {info.fullname}\n"
            f"Столица: {info.capital}\n"
            f"Расположение: {info.location}\n"
            f"Площадь: {info.square}\n"
            f"Язык: {info.language}\n"
            f"Население: {info.population}\n"
            f"Валюта: {info.currentcy}\n")
        await get_image(update, context)
    await update.message.reply_text(f"Продолжаем.")
    update_info()
    await update.message.reply_text(
        f"{info.capital}\n")
    return 3


async def third_response_capital(update, context):
    locality = update.message.text.title()
    global count, cor
    db_sess = db_session.create_session()
    con = db_sess.query(Country).filter((Country.name == locality) | (Country.fullname == locality) |
                                        (Country.english == locality))
    if list(con):
        await update.message.reply_text('Верно.')
        cor += 1
    else:
        await update.message.reply_text("Неверно.")
        count += 1
    if count < 2:
        await update.message.reply_text("Хотели бы Вы подробнее узнать о стране?")
        return 2
    await update.message.reply_text(f'Вы проиграли, Ваш результат: {cor}')
    user = User()
    user.user_name = update.effective_user.mention_html()
    user.type_game = "Столицы."
    user.score = cor
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    return ConversationHandler.END


async def first_response_flag(update, context):
    locality = update.message.text.title()
    global count, cor
    db_sess = db_session.create_session()
    con = db_sess.query(Country).filter((Country.name == locality) | (Country.fullname == locality) |
                                        (Country.english == locality))
    if list(con):
        await update.message.reply_text('Верно.')
        cor += 1
    else:
        await update.message.reply_text("Неверно.")
        count += 1
    if count < 2:
        await update.message.reply_text("Хотите ли вы узнать подробнее о стране?")
        return 2
    await update.message.reply_text(f'Вы проиграли, Ваш результат: {cor}.')
    user = User()
    user.user_name = update.effective_user.mention_html()
    user.type_game = "Флаги."
    user.score = cor
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    return ConversationHandler.END


async def second_response_flag(update, context):
    locality = update.message.text
    if locality.lower() == 'да':
        await update.message.reply_text(
            f"Название страны: {info.name}\n"
            f"Полное название страны: {info.fullname}\n"
            f"Столица: {info.capital}\n"
            f"Расположение: {info.location}\n"
            f"Площадь: {info.square}\n"
            f"Язык: {info.language}\n"
            f"Население: {info.population}\n"
            f"Валюта: {info.currentcy}\n")
    await update.message.reply_text(f"Продолжаем.")
    update_info()
    await get_image(update, context)  # Picture
    return 3


async def third_response_flag(update, context):
    locality = update.message.text.title()
    global count, cor
    db_sess = db_session.create_session()
    con = db_sess.query(Country).filter((Country.name == locality) | (Country.fullname == locality) |
                                        (Country.english == locality))
    if list(con):
        await update.message.reply_text('Верно.')
        cor += 1
    else:
        await update.message.reply_text("Неверно.")
        count += 1
    if count < 2:
        await update.message.reply_text("Хотели бы вы подробнее узнать о стране?")
        return 2
    await update.message.reply_text(f'Вы проиграли, Ваш результат: {cor}.')
    user = User()
    user.user_name = update.effective_user.mention_html()
    user.type_game = "Флаги."
    user.score = cor
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    return ConversationHandler.END


async def first_response_location(update, context):
    locality = update.message.text.title()
    global count, cor
    db_sess = db_session.create_session()
    con = db_sess.query(Country).filter((Country.location == locality) | (Country.location_precise == locality))
    if list(con):
        await update.message.reply_text('Верно.')
        cor += 1
    else:
        await update.message.reply_text("Неверно.")
        count += 1
    if count < 2:
        await update.message.reply_text("Хотите ли вы узнать подробнее о стране?")
        return 2
    await update.message.reply_text(f'Вы проиграли, Ваш результат: {cor}.')
    user = User()
    user.user_name = update.effective_user.mention_html()
    user.type_game = "Части света."
    user.score = cor
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    return ConversationHandler.END


async def second_response_location(update, context):
    locality = update.message.text
    if locality.lower() == 'да':
        await update.message.reply_text(
            f"Название страны: {info.name}\n"
            f"Полное название страны: {info.fullname}\n"
            f"Столица: {info.capital}\n"
            f"Расположение: {info.location}\n"
            f"Площадь: {info.square}\n"
            f"Язык: {info.language}\n"
            f"Население: {info.population}\n"
            f"Валюта: {info.currentcy}\n")
        await get_image(update, context)
    await update.message.reply_text(f"Продолжаем.")
    update_info()

    return 3


async def third_response_location(update, context):
    locality = update.message.text.title()
    global count, cor
    db_sess = db_session.create_session()
    con = db_sess.query(Country).filter((Country.location == locality) | (Country.location_precise == locality))
    if list(con):
        await update.message.reply_text('Верно.')
        cor += 1
    else:
        await update.message.reply_text("Неверно.")
        count += 1
    if count < 2:
        await update.message.reply_text("Хотели бы вы подробнее узнать о стране?")
        return 2
    await update.message.reply_text(f'Вы проиграли, Ваш результат: {cor}.')
    user = User()
    user.user_name = update.effective_user.mention_html()
    user.type_game = "Части света"
    user.score = cor
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    return ConversationHandler.END


async def get_image(update, context):
    url = f"https://flagcdn.com/w2560/{info.alpha2.lower()}.png"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            data = await r.read()
            await update.message.reply_photo(data)


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
        2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response_capital)],
        3: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_response_capital)]
    },
    fallbacks=[CommandHandler('stop', stop)]
)

flag_handler = ConversationHandler(
    entry_points=[CommandHandler('game_flag', game_flag)],
    states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response_flag)],
        2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response_flag)],
        3: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_response_flag)]
    },
    fallbacks=[CommandHandler('stop', stop)]
)

location_handler = ConversationHandler(
    entry_points=[CommandHandler('game_location', game_location)],
    states={
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response_location)],
        2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response_location)],
        3: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_response_location)],
    },
    fallbacks=[CommandHandler('stop', stop)])


def main():
    application = Application.builder().token("5847601109:AAHKlZOuGU7ZOX9yN8zW1b7a8wmU2zm8vPY").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("results", res))
    application.add_handler(flag_handler)
    application.add_handler(info_handler)
    application.add_handler(capital_handler)
    application.add_handler(location_handler)
    application.run_polling()


if __name__ == '__main__':
    create_table()
    main()
