from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler
)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update


def clean_callback(update, context):
    user_says = update.message.text
    res = " ".join([i for i in user_says.split() if 'абв' not in i.lower()])
    update.message.reply_text(f"Оригинальный текст: {user_says}\nОтформатированный текст: {res}")


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Если выхотите очистить текст от "абв" просто введите текст.\nЖелаете поиграть в игру с конфетами'
        ' /candy_game\nТак же вы можете воспользоваться калькулятором  /calc\n'
        'Хотите сыграть в BLACK JACK ? /init - начать играть, /yet - взять еще карту,'
        ' /stop - подведение итогов партиии'
    )
