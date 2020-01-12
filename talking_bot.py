from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
import logging
from src.hotdog import *
from src.util import *


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
    res = load_hit_signal(ref_date = '2020-01-10')
    print(res)
    
#   update.message.reply_text(res.shape[0])
#   update.message.reply_text(res.style.render(), parse_mode='HTML')
    some_html = """<html><style  type="text/css" >
</style><table id="T_8c339870_34f3_11ea_adac_0242ac110006" ><thead>    <tr>        <th class="blank level0" ></th>        <th class="col_heading level0 col0" >code</th>        <th class="col_heading level0 col1" >date</th>        <th class="col_heading level0 col2" >signal</th>        <th class="col_heading level0 col3" >hit</th>    </tr></thead><tbody>
                <tr>
                        <th id="T_8c339870_34f3_11ea_adac_0242ac110006level0_row0" class="row_heading level0 row0" >0</th>
                        <td id="T_8c339870_34f3_11ea_adac_0242ac110006row0_col0" class="data row0 col0" >1918</td>
                        <td id="T_8c339870_34f3_11ea_adac_0242ac110006row0_col1" class="data row0 col1" >2020-01-10 00:00:00</td>
                        <td id="T_8c339870_34f3_11ea_adac_0242ac110006row0_col2" class="data row0 col2" >s_bear_stick</td>
                        <td id="T_8c339870_34f3_11ea_adac_0242ac110006row0_col3" class="data row0 col3" >1</td>
            </tr>
    </tbody></table>  
</html>"""
    update.message.reply_text(some_html, parse_mode='HTML')

def table(bot, update):

   df = load_hit_signal(ref_date = '2020-01-10')
   table_html = parse_df(df)

   update.message.reply_text(table_html, parse_mode='HTML')

def table2(bot, update):
    html = """
    <table>
    <tbody>
    <tr><th>item  </th><th style="text-align: right;">  qty</th></tr>
    <tr><td>spam  </td><td style="text-align: right;">   42</td></tr>
    <tr><td>eggs  </td><td style="text-align: right;">  451</td></tr>
    <tr><td>bacon </td><td style="text-align: right;">    0</td></tr>
    </tbody>
    </table>
    """
    update.message.reply_text(html, parse_mode='HTML')
   
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
    dp.add_handler(CommandHandler("table2", table2))
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
