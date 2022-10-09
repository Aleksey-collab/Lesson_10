from game import *
from functions import *
from calc import *
from black_jack import *
from config import API_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    TOKEN = API_TOKEN
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    init_handler = CommandHandler('init', init)
    st_handler = CommandHandler('yet', yet)
    sto_handler = CommandHandler('stop', stop)
    init_handler = CommandHandler('score', score)

    conv_handler_calc = ConversationHandler(
        entry_points=[CommandHandler('calc', init_calc)],
        states={
            INPUT: [MessageHandler(Filters.text, input_value)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    # Добавляем обработчик калькулятора `conv_handler_calc`
    dispatcher.add_handler(conv_handler_calc)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('candy_game', game_start)],
        states={
            STEP_PL: [MessageHandler(Filters.text, step_player)],
            STEP_BOT: [MessageHandler(Filters.text, step_bot)],
            END_GAME: [MessageHandler(Filters.text, end_game)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    # Добавляем обработчик игры `conv_handler`
    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(init_handler)
    dispatcher.add_handler(st_handler)
    dispatcher.add_handler(sto_handler)

    dispatcher.add_handler(MessageHandler(Filters.text, clean_callback))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
