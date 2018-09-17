from database.db_wrapper import DBwrapper
from threading import Thread
from main import logger, stop_and_restart

def admin_method(func):
    """Decorator for marking methods as admin-only methods, so that strangers can't use them"""

    def admin_check(bot, update):
        db = DBwrapper.get_instance()
        user = update.message.from_user
        if user.id in db.get_admins():
            return func(bot, update)
        else:
            update.message.reply_text('You have not the needed permissions to do that!')
            logger.warning(
                "User {} ({}, @{}) tried to use admin function '{}'!".format(user.id, user.first_name, user.username,
                                                                             func.__name__))

    return admin_check

@admin_method
def restart(bot, update):
    update.message.reply_text('Bot is restarting...')
    Thread(target=stop_and_restart).start()