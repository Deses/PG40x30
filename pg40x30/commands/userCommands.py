import logging

from pg40x30 import keyboards

from telegram import MessageEntity
from telegram import ParseMode
from telegram import constants as t_consts

from lang.language import translate
from database.db_wrapper import DBwrapper

logger = logging.getLogger(__name__)


# **************
# Tools
# **************
def deleteMessage(bot, update, quantity=0):
    if update.callback_query is not None:
        upd = update.callback_query
    elif update is not None:
        upd = update

    bot.delete_message(chat_id=upd.message.chat_id,
                       message_id=upd.message.message_id - quantity
                       )


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
    deleteMessage(bot, update)


def addUser(bot, update):
    text = translate("registerMsg")
    keyboard = keyboards.getUserKeyboard()
    bot.sendMessage(chat_id=update.message.chat_id,
                    message_id=update.message.message_id,
                    text=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=keyboard
                    )
    deleteMessage(bot, update)


def confirmNewUser(bot, update):
    query = update.callback_query

    if query.data == "cancel":
        deleteMessage(bot, update)
    else:
        user = query.from_user
        try:
            db = DBwrapper.get_instance()
            db.add_user(user.id, user.first_name, user.last_name, user.username, query.data, user.language_code)
        except Exception as ex:
            logger.error("confirmNewUser - An error has occurred while adding an user!", ex)
        else:
            text = translate("registryConfirmationMsg").format(user.username, query.data)
            bot.edit_message_text(text=text,
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

    bot.sendMessage(chat_id=update.message.chat_id,
                    message_id=update.message.message_id,
                    text=finalString,
                    parse_mode=ParseMode.HTML,
                    )
    deleteMessage(bot, update)


def addAlertToUserProfile(bot, update):
    user = update.effective_user

    text = translate("alertMsg").format(user.username)
    keyboard = keyboards.getProfileKeyboard()
    bot.sendMessage(chat_id=update.message.chat_id,
                    message_id=update.message.message_id,
                    text=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=keyboard
                    )

    deleteMessage(bot, update)


def saveAlertToUserProfile(bot, update):
    query = update.callback_query

    if query.data == "cancel":
        deleteMessage(bot, update)
    else:
        user = query.from_user
        try:
            db = DBwrapper.get_instance()
            db.add_user_profile(user.id, query.data)
        except Exception as ex:
            logger.error("saveAlertToUserProfile - An error has occurred while saving a profile!", ex)
        else:
            text = translate("alertConfirmationMsg").fomat(user.username)
            bot.edit_message_text(text=text,
                                  parse_mode=ParseMode.HTML,
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id)


def getUserProfle(bot, update):
    text = translate("userInfoMsg")
    keyboard = keyboards.getUserKeyboard()
    bot.sendMessage(chat_id=update.message.chat_id,
                    message_id=update.message.message_id,
                    text=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=keyboard
                    )

    deleteMessage(bot, update)


def showUserProfile(bot, update):
    query = update.callback_query

    if query.data == "cancel":
        deleteMessage(bot, update)
    else:
        user = query.from_user
        try:
            db = DBwrapper.get_instance()
            userProfiles = db.get_user_profile()
        except Exception as ex:
            logger.error("showUserProfile - An error has occurred while getting  an user profile!", ex)
        else:
            text = translate("registryConfirmationMsg")
            bot.edit_message_text(text=text.format(user.username, query.data),
                                  parse_mode=ParseMode.HTML,
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id)