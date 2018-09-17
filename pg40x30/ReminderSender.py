# import logging
# import telegram
# from telegram.ext import Updater
#
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
#
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
#
# API_KEY = open('assets/.api_key').read()
#
# bot = telegram.Bot(API_KEY)
# updater = Updater(API_KEY)
#
# jobQueue = updater.job_queue
#
# def callback_minute(bot, job):
#     bot.send_message(chat_id='@desesTestBot', text='One message every minute')
#
# job_minute = jobQueue.run_repeating(callback_minute, interval=5, first=0)
#
#
# updater.start_polling()
