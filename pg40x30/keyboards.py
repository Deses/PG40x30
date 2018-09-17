from builtins import print

from constants.buttons import userNumbers
from constants.buttons import userNumberCancel

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


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
    buttons = list()
    for userNumber in userNumbers:
        buttons.append(
            InlineKeyboardButton(text=str(userNumber), callback_data="register_user")
        )

    lastRowButton = [
        InlineKeyboardButton(text=str(userNumberCancel), callback_data="cancel_user_registration")
    ]

    # button_list = [[InlineKeyboardButton(text=user, callback_data="join_game")] for user in userNumbers]
    reply_mrk = InlineKeyboardMarkup(build_menu(buttons, n_cols=4, footer_buttons=lastRowButton))
    # update.message.reply_text(reply_msg, reply_markup=reply_mrk)

    # keyboard = InlineKeyboardMarkup(reply_mrk, one_time_keyboard=True)
    # return keyboard
    return reply_mrk