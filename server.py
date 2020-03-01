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
# Real commands     #  
#####################

@typing    
def signal(update, context):

    # Get the first argument as input date
    input_str = update.message.text
    if(len(input_str.split()) > 1):
        input_str = input_str.split()[1]  # First argument
    else:
        input_str = None

    ref_date_str = format_input_date(input_str)
    df_signal = LoadHitSignal(ref_date = ref_date_str)

    # If dataframe, else return error message
    if isinstance(df_signal, pd.DataFrame):
        # Create signal mapping dataframe
        mapping = [['s_bull_stick', "\u5927\u967d\u71ed"],
                   ['s_bear_stick', "\u5927\u9670\u71ed"],
                   ['s_bull_engulf', "\u5411\u597d\u541e\u566c"],
                   ['s_bear_engulf', "\u5411\u6de1\u541e\u566c"],
                   ['s_bull_harami', "\u5411\u597d\u8eab\u61f7\u516d\u7532"],
                   ['s_bear_harami', "\u5411\u6de1\u8eab\u61f7\u516d\u7532"],
                   ['s_2day_reverse_good', "\u5411\u597d\u96d9\u65e5\u8f49\u5411"],
                   ['s_2day_reverse_bad', "\u5411\u6de1\u96d9\u65e5\u8f49\u5411"],
                   ['s_bull_pierce', "\u66d9\u5149\u521d\u73fe"],
                   ['s_bear_pierce', "\u70cf\u96f2\u84cb\u9802"],
                   ['s_hammer', "\u939a\u982d"],
                   ['s_shooting_star', "\u5c04\u64ca\u4e4b\u661f"]] 
        df_map  = pd.DataFrame(mapping, columns = ['signal', 'signal_label'])

        # Load hit signal, map signal label
        df_res = df_signal.merge(df_map, on='signal', how='left')
        df_res = df_res[['code', 'date', 'signal_label']]

        # Print dataframe
        df_str = print_df(df_res)

        update.message.reply_text(df_str, parse_mode = ParseMode.HTML)

    else:
        err = df_signal.decode("utf-8")
        update.message.reply_text(err, parse_mode = ParseMode.HTML)
        
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
    dp.add_handler(CommandHandler("s", signal))       # Overloading with /s command

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

