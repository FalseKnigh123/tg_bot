import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот, который поможет тебе подтянуть свои знания по географии и хорошо"
        rf" провести время) Напишите мне что-нибудь, и я пришлю это назад!",
    )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Напишем всеокой фигни") # TO Do: написать что-то


async def echo(update, context):
    await update.message.reply_text(update.message.text)
    print(update.message.text)


def main():
    application = Application.builder().token("6211811458:AAE10kS4o9HfzHTQa_uGXHaWXuqu2bia83A").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
