import logging
from functools import wraps
from src.hotdog import *
from src.util import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction, ParseMode
import pandas as pd
import wikipedia

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
@typing
def fun(update, context):
    """Send a message when the command /start is issued."""

    input_str = update.message.text
    if(len(input_str.split()) > 1):
        query_str = input_str.split()[1]  # First argument
    else:
        query_str = "Apple"

    res = wikipedia.summary(query_str)
    res = u''.join(res).encode('utf-8').strip()

    update.message.reply_text(res)

@typing
def test(update, context):
    """Send a message when the command /test is issued."""

    df = GetSignalPerformance(code = '2333')
    df = map_signal(df)
    table_html = print_df(df)

    update.message.reply_text(table_html)

@typing
def testing(update, context):
    """Send a message when the command /testing is issued."""
    s = pd.Series(list('abca'))
    ss = pd.get_dummies(s)

    b = ss.apply(random_print, axis=1)

    msg = "\n".join(b.tolist())

    msg = "<u> Something </u> \n\n" + msg
    update.message.reply_text(msg, parse_mode = ParseMode.HTML)

@typing
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

@typing
def dummy(update, context):

    df_history = GetSignalPerformance(code = '2333')
    df_history = map_signal(df_history)

    df_history_str = df_history.groupby(['signal']).apply(lambda ss: print_history_df(ss))
    res_str = '\n'.join(df_history_str.tolist())

    update.message.reply_text(res_str, parse_mode = ParseMode.HTML)

#####################
# Real commands     #  
#####################

@typing
def status(update, context):
    df_status = check_cronjob()
    df_status_str = print_df(df_status, bold = ['table', 'date'])

    update.message.reply_text(df_status_str, parse_mode = ParseMode.HTML)


@typing    
def signal(update, context):

    # Get the first argument as input date
    input_str = update.message.text
    logger.info(input_str)
    if(len(input_str.split()) > 1):
        input_str = input_str.split()[1]  # First argument
    else:
        input_str = None

    ref_date_str = format_input_date(input_str)
    df_signal = LoadHitSignal(ref_date = ref_date_str)

    # If dataframe, else return error message
    if isinstance(df_signal, pd.DataFrame):

        # map signal key to signal_label
        df_res = map_signal(df_signal)

        # Print dataframe
        df_str = print_df(df_res)

        update.message.reply_text(df_str, parse_mode = ParseMode.HTML)

    else:
        err = df_signal.decode("utf-8")
        update.message.reply_text(err, parse_mode = ParseMode.HTML)

@typing
def history(update, context):

    df_history = GetSignalPerformance(code = '2333')
    df_history = map_signal(df_history)

    df_history_str = df_history.groupby(['signal']).apply(lambda ss: print_history_df(ss))
    res_str = '\n'.join(df_history_str.tolist())

    update.message.reply_text(res_str, parse_mode = ParseMode.HTML)

        
@typing    
def hello(update, context):

    # Create signal mapping dataframe
    mapping = [['s_bear_stick', "\u5927\u967d\u71ed"]] 
    df_map  = pd.DataFrame(mapping, columns = ['signal', 'signal_label'])

    # Load hit signal, map signal label
    df_signal = load_hit_signal(ref_date = '2020-01-10')
    df_res = df_signal.merge(df_map, on='signal', how='left')

    # Print dataframe
    df_str = print_df(df_res)
    
    update.message.reply_text(df_str, parse_mode = ParseMode.HTML)

    
#####################
# Main              #  
#####################
    

def main():
    updater = Updater("589160362:AAHEeNBIeh3m3RA07lANaDHovy874xNFi1g", use_context = True)

    # Dispatcher add handlers
    dp = updater.dispatcher

    # Some init commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # Dummy commands
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("testing", testing))
    dp.add_handler(CommandHandler("t", testing))
    dp.add_handler(CommandHandler("dummy", dummy))
    dp.add_handler(CommandHandler("hello", hello))
    dp.add_handler(CommandHandler("fun", fun))
    dp.add_handler(CommandHandler("ff", fun))
    

    # Real commands
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("signal", signal))
    dp.add_handler(CommandHandler("history", history))

    # Overload command
    dp.add_handler(CommandHandler("s", signal))       # Overloading with /s command
    dp.add_handler(CommandHandler("h", history))      # Overloading with /h command
    

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

