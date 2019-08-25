import os
import sys
from threading import Thread
from saturnbot import updater
from telegram.ext import Updater
from saturn_key import telegram_key

updater = Updater(token=telegram_key)


def stop_and_restart():
    updater.stop()
    os.execl(sys.executable, sys.executable, * sys.argv)
    

def restart(bot, update):
    update.message.reply_text('Bot is restarting...')
    Thread(target=stop_and_restart).start()