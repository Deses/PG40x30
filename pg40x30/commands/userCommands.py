from pg40x30 import keyboards

from telegram import MessageEntity
from telegram import ParseMode
from telegram import constants as t_consts

from lang.language import translate, translate_all

# **************
# User commands
# **************
def start(bot, update):
    text = translate("welcomeMsg")
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)


def register_user(bot, update):
    text = translate("registerMsg")
    keyboard = keyboards.getUserKeyboard()
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)