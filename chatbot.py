from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


import configparser
import logging
import redis

# import firebase_admin
# cred = credentials.Certificate('comp7940-cook-21414122.json')
# 初始化firebase，注意不能重複初始化
# firebase_admin.initialize_app(cred)
# 初始化firestore
# db = firestore.client()

global redis1

def main():
    # Load your token and create an Updater for your Bot
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    global redis1
    redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']), port=(config['REDIS']['PORT']))

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("find", find_command))
    dispatcher.add_handler(CommandHandler("share", share_command))

    # To start the bot:
    updater.start_polling()
    updater.idle()

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Tips: the command /find <FoodNetwork/BettyCrocker/Allrecipes/MarthaStewart> shows the cook website. ---------------------                    The command /share <YouTube/Twitter> shows the sharing platforms')

def find_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /find is issued."""
    try: 
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        if msg == 'FoodNetwork':
            update.message.reply_text('Here is the link for FoodNetwork: https://www.foodnetwork.com/')   
        elif msg == 'BettyCrocker':   
            update.message.reply_text('Here is the link for BettyCrocker: https://www.bettycrocker.com/') 
        elif msg == 'Allrecipes':   
            update.message.reply_text('Here is the link for Allrecipes: https://www.allrecipes.com/') 
        elif msg == 'MarthaStewart':   
            update.message.reply_text('Here is the link for MarthaStewart: https://www.marthastewart.com/1503096/videos') 
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /find <FoodNetwork/BettyCrocker/Allrecipes/MarthaStewart>')

def share_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /share is issued."""
    try: 
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        if msg == 'YouTube':
            update.message.reply_text('Here is the link for sharing: https://www.youtube.com/')   
        elif msg == 'Twitter':   
            update.message.reply_text('Here is the link for sharing: https://twitter.com/') 
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /share <YouTube/Twitter>')


if __name__ == '__main__':
    main()