import logging
from functools import wraps
from src.hotdog import *
from src.util import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction, ParseMode

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#####################
# Decorator         #  
#####################
def typing(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func

#####################
# Testing           #  
#####################

def test(update, context):
    """Send a message when the command /test is issued."""

    df = load_hit_signal(ref_date = '2020-01-10')
    table_html = print_df(df)

    update.message.reply_text(table_html)

@typing
def testing(update, context):
    """Send a message when the command /testing is issued."""
    update.message.reply_text('Testing!')

@typing
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

@typing
def status(update, context):
    df_status = check_cronjob()
    df_status_str = print_df(df_status, bold = ['table', 'date'])

    update.message.reply_text(df_status_str, parse_mode = ParseMode.HTML)

@typing
def dummy(update, context):

    df = load_hit_signal(ref_date = '2020-01-10')
    df_str = print_df(df)
    # df = check_cronjob()
    # msg = print_df(df, bold = ['table', 'date'])

    update.message.reply_text(df_str, parse_mode = ParseMode.HTML)
    
#####################
# Main              #  
#####################
    

def main():
    updater = Updater("589160362:AAHEeNBIeh3m3RA07lANaDHovy874xNFi1g", use_context = True)

    # Dispatcher add handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("testing", testing))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("dummy", dummy))
    
    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

