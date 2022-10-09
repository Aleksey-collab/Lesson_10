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


# Определяем константы этапов ИГРЫ
STEP_PL, STEP_BOT, END_GAME = range(3)
DATA_SET = ['', '', 100, 28, 0, '']


def update_game_data(val):
    global DATA_SET
    DATA_SET = val


def game_start(update, _):
    user = update.message.from_user
    data = DATA_SET

    update.message.reply_text(
        f'Привет {user.first_name}, '
        'Меня зовут Профессор. Я сыграю с вами в игру. '
        'Команда /cancel, чтобы прекратить игру.\n\n'
        )

    player_1 = user.first_name
    player_2 = 'Профессор'
    all_canndy = data[2]
    max_canndy = data[3]
    candy = data[2]
    win_player = data[5]
    crete_data = [player_1, player_2, all_canndy, max_canndy, candy, win_player]
    f_move = random.choice((player_1, player_2))

    #update data
    update_game_data(crete_data)

    if player_1 == f_move:
        update.message.reply_text(
            f'Ходит: {player_1}, конфет осталось {candy} '
            f'введите число от 1 до {max_canndy}'
        )
        return STEP_PL
    else:
        update.message.reply_text(
            f'Начало игры первым ходит: {f_move} '
            'для продолжения нажмите любую клавишу-->'
        )
        return STEP_BOT


def step_player(update, _):
    user = update.message.from_user
    # get_game_data
    data = DATA_SET
    player_1 = data[0]
    candy = data[4]
    win_player = data[5]

    k = update.message.text

    try:
        candy -= int(k)
    except:
        update.message.reply_text(
            f'Вы ввнли некоректные данные, пожалуйста введите цифру от 1 до 28'
        )
        return STEP_PL

    logger.info("ход %s: взял конфет %s", player_1, k)

    update.message.reply_text(
        f'Игрок {player_1} берет {k} конфет, всего осталось {candy}'
    )

    crete_data = [data[0], data[1], data[2], data[3], candy, win_player]

    # update data
    update_game_data(crete_data)

    if candy <= 0:
        win_player = player_1

    if win_player:
        crete_data = [data[0], data[1], data[2], data[3], 100, win_player]

        # update data
        update_game_data(crete_data)

        return END_GAME
    else:
        player_2 = data[1]
        update.message.reply_text(
            f'Ходит: {player_2}, конфет осталось {candy} '
            f'для продолжения нажмите любую кнопку'
        )
        return STEP_BOT


def step_bot(update, _):
    user = update.message.from_user
    # get_game_data
    data = DATA_SET
    player_2 = data[1]
    max_canndy = data[3]
    candy = data[4]
    win_player = data[5]

    logger.info("Ход %s: взял конфет %s", player_2, update.message.text)

    x = candy % max_canndy
    if x != 0:
        if (candy - x) > max_canndy and (candy - max_canndy) > max_canndy:
            candy -= x
            update.message.reply_text(
                f'Профессор берет {x} конфет, всего осталось {candy}'
            )
        elif 0 < candy <= max_canndy:
            l = candy
            candy -= candy
            win_player = player_2
            update.message.reply_text(
                f'Профессор берет {l} конфет, всего осталось {candy}'
            )
        else:
            candy -= 1
            update.message.reply_text(
                f'Профессор берет {1} конфет, всего осталось {candy}'
            )
    else:
        if (candy - x) > max_canndy and (candy - max_canndy) > max_canndy:
            candy -= max_canndy
            update.message.reply_text(
                f'Профессор берет {max_canndy} конфет, всего осталось {candy}'
            )
        elif 0 < candy <= max_canndy:
            l = candy
            candy -= candy
            win_player = player_2
            update.message.reply_text(
                f'Профессор берет {l} конфет, всего осталось {candy}'
            )
        else:
            candy -= 1
            update.message.reply_text(
                f'Профессор берет {1} конфет, всего осталось {candy}'
            )
    crete_data = [data[0], data[1], data[2], data[3], candy, win_player]
    # update data
    update_game_data(crete_data)
    if win_player:
        crete_data = [data[0], data[1], data[2], data[3], 100, win_player]
        # update data
        update_game_data(crete_data)
        return END_GAME
    else:
        player_1 = data[0]
        max_canndy = data[3]
        update.message.reply_text(
            f'Ходит: {player_1}, конфет осталось {candy} '
            f'введите число от 1 до {max_canndy}'
        )
        return STEP_PL


def end_game(update, _):
    user = update.message.from_user
    # get_game_data
    data = DATA_SET
    win_player = data[5]
    logger.info("Выиграл %s", win_player)

    update.message.reply_text(
        f'Выиграл {win_player}'
    )
    # prepare new game
    crete_data = ['', '', data[2], data[3], 100, '']
    # update data
    update_game_data(crete_data)
    return ConversationHandler.END


def cancel(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s отменил разговор.", user.first_name)

    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        ' Будет скучно - пиши.'
    )

    return ConversationHandler.END
