import random
import logging
from telegram.ext import (
    ConversationHandler,
)


# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)



INPUT = range(1)
res = 0


def init_calc(update, _):
    update.message.reply_text(f"Введите пример для расчета(ПРИМЕР: 1+1 or 123424*2 or 123/3)")
    return INPUT


def input_value(update, _):
    data = update.message.text
    global res
    res = eval(data)
    update.message.reply_text(f"результат: {round(res,2)}\n для продолжения нажимте любую кнопку")
    logger.info("введен пример: %s, результат: %s", data, res)
    return ConversationHandler.END
