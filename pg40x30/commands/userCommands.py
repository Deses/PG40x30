import logging

from pg40x30 import keyboards

from telegram import MessageEntity
from telegram import ParseMode
from telegram import constants as t_consts

from lang.language import translate
from database.db_wrapper import DBwrapper

logger = logging.getLogger(__name__)


# **************
# User commands
# **************
def start(bot, update):
    text = translate("welcomeMsg")
    bot.sendMessage(chat_id=update.message.chat_id,
                    message_id=update.message.message_id,
                    text=text,
                    parse_mode=ParseMode.HTML
                    )
    bot.delete_message(chat_id=update.message.chat_id,
                       message_id=update.message.message_id
                       )


def addUser(bot, update):
    text = translate("registerMsg")
    keyboard = keyboards.getUserKeyboard()
    bot.sendMessage(chat_id=update.message.chat_id,
                    message_id=update.message.message_id,
                    text=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=keyboard
                    )
    bot.delete_message(chat_id=update.message.chat_id,
                       message_id=update.message.message_id
                       )


def confirmNewUser(bot, update, chat_data):
    query = update.callback_query

    if query.data == "cancel":
        bot.delete_message(chat_id=query.message.chat_id,
                           message_id=query.message.message_id)
    else:
        user = query.from_user
        try:
            db = DBwrapper.get_instance()
            db.add_user(user.id, user.first_name, user.last_name, user.username, query.data, user.language_code)
        except Exception as ex:
            logger.error("An error has occurred while adding an user!", ex)
        else:
            text = translate("registryConfirmationMsg")
            bot.edit_message_text(text=text.format(user.username, query.data),
                                  parse_mode=ParseMode.HTML,
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id)


def getRegisteredUsers(bot, update):
    db = DBwrapper.get_instance()
    userList = db.get_all_users()

    header = translate("userListMsg1")
    footer = translate("userListMsg3")

    formatedUserList = []
    for user in userList:
        formatedUserList.append(translate("userListMsg2").format(f'{user[5]:02}', user[4]))

    finalString = header + "\n\n"
    finalString += '\n'.join(formatedUserList)
    finalString += "\n\n" + footer

    update.message.reply_text(
        text=finalString,
        parse_mode=ParseMode.HTML,
    )
