from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from database.db_wrapper import DBwrapper
from lang.language import translate


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def getUserKeyboard():
    db = DBwrapper.get_instance()
    usedNumbers = [x[0] for x in db.get_used_numbers()]

    allNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                  26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41]

    availableNumbers = [x for x in allNumbers if x not in usedNumbers]

    buttons = list()
    for userNumber in availableNumbers:
        buttons.append(
            InlineKeyboardButton(text=str(userNumber).zfill(2), callback_data=str(userNumber))
        )

    lastRowButton = [
        InlineKeyboardButton(text=translate("cancelMsg"), callback_data="cancel")
    ]

    # button_list = [[InlineKeyboardButton(text=user, callback_data="join_game")] for user in userNumbers]
    reply_mrk = InlineKeyboardMarkup(
        build_menu(buttons, n_cols=4, footer_buttons=lastRowButton),
        one_time_keyboard=False
    )
    # update.message.reply_text(reply_msg, reply_markup=reply_mrk)

    # keyboard = InlineKeyboardMarkup(reply_mrk, one_time_keyboard=True)
    # return keyboard
    return reply_mrk
