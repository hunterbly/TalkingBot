from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
import logging
from datetime import date, datetime
from src.hotdog import *
from src.util import *
import pandas as pd

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

STEP_ONE, LUNCH = range(2)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def lunch(bot, update):
    """Send a message when the command /lunch is issued."""
    update.message.reply_text('Where should i be having lunch ffs')

def step_one(bot, update):
    user = update.message.from_user
    logger.info("Input: %s", update.message.text)
    update.message.reply_text('Hey you. \n\n And Your input is %s' % update.message.text)

    return ConversationHandler.END

def signal(bot, update):
    # reply_keyboard = [['Signal'], ['Options'], ['CCASS']]
    reply_keyboard = [['Signal', 'Options', 'CCASS']]


    update.message.reply_text(
        'Hi! This is some keyboards. \n\n'
        'Send /cancel to stop talking to me.\n\n'
        'What are you looking for?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return STEP_ONE

def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Test Hi!')

def test(bot, update):

    # Try parsing user input 
    input_str = update.message.text

    if(len(input_str.split()) > 1):
       input_str = input_str.split()[1]  # First argument
       
    else:
       input_str = date.today().strftime("%Y%m%d")
       
    try:
       ref_date = datetime.strptime(input_str, '%Y%m%d')
       ref_str = ref_date.strftime('%Y-%m-%d')
       print(ref_str)
       
       df = load_hit_signal(ref_date = ref_str)

       if isinstance(df, pd.DataFrame):
           table_html = parse_df(df)
           update.message.reply_text(table_html, parse_mode='HTML')
       else:
           err_msg = df.decode("utf-8")
           update.message.reply_text(err_msg)
       
    except Exception as e:
        print(e)
        error = 'Please input date in YYYYMMDD format'
        update.message.reply_text(error)

def table(bot, update):

   df = load_hit_signal(ref_date = '2020-01-10')
   df.drop(columns=['date'], axis = 1, inplace=True, errors='ignore')  # drop id column if exists

   table_html = parse_df(df)

   update.message.reply_text(table_html, parse_mode='HTML')

   
def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    text = update.message.text + " what"
    update.message.reply_text(text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope you earn a lot from that ffs.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("589160362:AAHEeNBIeh3m3RA07lANaDHovy874xNFi1g")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("table", table))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("lunch", lunch))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('signal', signal)],

        states={
            STEP_ONE: [RegexHandler('^(Signal|Options|CCASS)$', step_one)]


        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
