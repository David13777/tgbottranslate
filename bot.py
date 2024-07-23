import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from translate import Translator

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Ваш токен Telegram бота
TOKEN = '7239900154:AAGf0jPi0AWOTeat9uhvxNTPdOpfK0tNSXs'

# Поддерживаемые языки
LANGUAGES = {
    'en': 'English',
    'ru': 'Russian',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean'
}


# Функция для перевода текста с использованием библиотеки translate
def translate_text(text, target_language='en'):
    translator = Translator(to_lang=target_language)
    try:
        translated_text = translator.translate(text)
    except Exception as e:
        logging.error(f"Ошибка перевода: {e}")
        return 'Ошибка перевода'
    return translated_text


# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Привет! Отправь мне текст для перевода и укажи целевой язык. Пример: /translate ru Hello')


# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Доступные команды:\n'
        '/start - Начать работу с ботом\n'
        '/help - Показать это сообщение\n'
        '/language - Показать список поддерживаемых языков\n'
        '/translate <target_language> <text> - Перевести текст на целевой язык\n'
    )


# Обработчик команды /language
async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    languages = ', '.join([f'{code} ({name})' for code, name in LANGUAGES.items()])
    await update.message.reply_text(f'Поддерживаемые языки: {languages}')


# Обработчик команды /translate
async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            'Пожалуйста, укажите целевой язык и текст для перевода. Пример: /translate ru Hello')
        return

    target_language = context.args[0]
    if target_language not in LANGUAGES:
        await update.message.reply_text('Неподдерживаемый язык. Поддерживаемые языки: ' + ', '.join(LANGUAGES.keys()))
        return

    text_to_translate = ' '.join(context.args[1:])
    translated_text = translate_text(text_to_translate, target_language=target_language)
    await update.message.reply_text(translated_text)


def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("language", language))
    application.add_handler(CommandHandler("translate", translate))

    # Запускаем бота
    application.run_polling()


if __name__ == '__main__':
    main()
