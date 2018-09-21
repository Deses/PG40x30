import logging
import os
import re
import sys

from telegram import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,  CallbackQueryHandler
from commands import userCommands

from lang.language import translate, translate_all

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# -----------------
# Internal methods
# -----------------




# Gracefully stops the Updater and replaces the current process with a new one
def stop_and_restart():
    updater.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)


# -----------------
# Main
# -----------------
def main():
    API_KEY = open('constants/.api_key').read()
    global updater
    updater = Updater(token=API_KEY)
    dispatcher = updater.dispatcher


    # -----------------
    # Handlers
    # -----------------
    # channel_handler = MessageHandler(own_filters.ChannelFilter, leave_chat)
    start_handler = CommandHandler(translate_all("startCmd"), userCommands.start)
    register_handler = CommandHandler(translate_all("registerCmd"), userCommands.addUser)
    confirmation_handler = CallbackQueryHandler(userCommands.confirmNewUser, pass_chat_data=True)
    # stop_handler = CommandHandler(translate_all("stopCmd"), stop_cmd)
    # join_handler = CommandHandler(translate_all("join"), join_cmd)
    # help_handler = CommandHandler('help', help_cmd)
    # hide_handler = CommandHandler('hide', hide_cmd)
    getRegisteredUsers_handler = CommandHandler(translate_all("usersCmd"), userCommands.getRegisteredUsers)
    # language_handler = CommandHandler('language', language_cmd)
    # comment_handler = CommandHandler('comment', comment_cmd, pass_args=True)
    # callback_handler = CallbackQueryHandler(callback_eval)
    # users_handler = CommandHandler('users', users)
    # answer_handler = CommandHandler('answer', answer)
    # restart_handler = CommandHandler('restart', restart)

    # game_command_handler = MessageHandler(Filters.text, game_commands)

    # mp_handler = CommandHandler('multiplayer', multiplayer)
    # join_sec = CommandHandler('join_secret', join_secret)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(register_handler)
    dispatcher.add_handler(confirmation_handler)
    dispatcher.add_handler(getRegisteredUsers_handler)
    # dispatcher.add_handler(callback_handler)

    updater.start_polling()
    logger.info("Bot started as @{}".format(updater.bot.username))
    updater.idle()


if __name__ == '__main__':
    main()