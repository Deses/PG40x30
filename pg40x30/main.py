import logging
import os
import re
import sys

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from commands import userCommands, botHelper
from lang.language import translate_all


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# -----------------
# Internal methods
# -----------------
def callback_eval(bot, update):
    query_data = update.callback_query.data

    # For changing the language:
    if query_data.startswith("ch_lang"):
        lang_id = re.search("ch_lang_([a-z]{2})", query_data).group(1)
        # change_language(bot=bot, update=update, lang_id=lang_id)

    # elif query_data == "com_ch_lang":
        # language_cmd(bot, update)

    # elif query_data == "cancel_comment":
        # cancel_cmd(bot, update)

    elif query_data == "register_user":
        print(update.callback_query.data)

        bot.answerCallbackQuery(callback_query_id=update.callback_query.id)
        botHelper.add_user(bot, update)
    # elif query_data == "cancel_user_registration":
        #     bot.answerCallbackQuery(callback_query_id=update.callback_query.id)
        # start_cmd(bot, update)


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
    register_handler = CommandHandler(translate_all("registerCmd"), userCommands.register_user)
    # stop_handler = CommandHandler(translate_all("stopCmd"), stop_cmd)
    # join_handler = CommandHandler(translate_all("join"), join_cmd)
    # help_handler = CommandHandler('help', help_cmd)
    # hide_handler = CommandHandler('hide', hide_cmd)
    # stats_handler = CommandHandler('stats', stats_cmd)
    # language_handler = CommandHandler('language', language_cmd)
    # comment_handler = CommandHandler('comment', comment_cmd, pass_args=True)
    callback_handler = CallbackQueryHandler(callback_eval)
    # users_handler = CommandHandler('users', users)
    # answer_handler = CommandHandler('answer', answer)
    # restart_handler = CommandHandler('restart', restart)

    # game_command_handler = MessageHandler(Filters.text, game_commands)

    # mp_handler = CommandHandler('multiplayer', multiplayer)
    # join_sec = CommandHandler('join_secret', join_secret)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(register_handler)
    dispatcher.add_handler(callback_handler)

    print("holi")
    print(translate_all("registerCmd"))
    updater.start_polling()
    logger.info("Bot started as @{}".format(updater.bot.username))
    updater.idle()


if __name__ == '__main__':
    main()