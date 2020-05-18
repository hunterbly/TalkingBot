from src.logger import setup_logger
from functools import wraps
from src.hotdog import GetSignalPerformance, check_cronjob, LoadHitSignal

from src.util import parse_telegram_input, map_signal, print_df, random_print, \
                     format_input_date, print_history_df

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction, ParseMode
import pandas as pd


#####################
# Decorator         #
#####################


def typing(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):

        context.bot.send_chat_action(chat_id=update.effective_message.chat_id,
                                     action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func

#####################
# Testing           #
#####################
@typing
def fun(update, context):
    """Send a message when the command /start is issued."""

    res = 'ABC'

    update.message.reply_text(res)


@typing
def test(update, context):
    """Send a message when the command /test is issued."""

    df = GetSignalPerformance(code='2333')
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
    update.message.reply_text(msg, parse_mode=ParseMode.HTML)


@typing
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


@typing
def dummy(update, context):

    input_str = update.message.text

    res_str = parse_telegram_input(input_str, 1)

    update.message.reply_text(res_str, parse_mode=ParseMode.HTML)

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
    input_str = parse_telegram_input(input_str, 1)
    ref_date_str = format_input_date(input_str)

    df_signal = LoadHitSignal(ref_date=ref_date_str)

    # If dataframe, else return error message
    if isinstance(df_signal, pd.DataFrame):

        # map signal key to signal_label
        df_res = map_signal(df_signal)

        # Print dataframe
        df_str = print_df(df_res)

        update.message.reply_text(df_str, parse_mode=ParseMode.HTML)

    else:
        err = df_signal.decode("utf-8")
        update.message.reply_text(err, parse_mode=ParseMode.HTML)


@typing
def history(update, context):

    # Get the first argument as stock code
    input_str = update.message.text
    code = parse_telegram_input(input_str, 1)

    df_history = GetSignalPerformance(code=code)
    df_history = map_signal(df_history)

    # Add sorting so the latest signal is at the top
    df_history = df_history.sort_values(by=['date'], ascending=False).reset_index(drop=True, inplace=False)
    df_history['date'] = df_history['date'].apply(lambda x: x.strftime("%d-%b-%y"))  # Date to string

    df_history_str = df_history.groupby(['signal'], sort=False).apply(lambda ss: print_history_df(ss))
    res_str = '\n'.join(df_history_str.tolist())

    update.message.reply_text(res_str, parse_mode=ParseMode.HTML)


@typing
def hello(update, context):

    df_str = "Hello"

    update.message.reply_text(df_str, parse_mode=ParseMode.HTML)


@typing
def todo(update, context):

    """ Simply display content in the todo file or add new append new ones for review"""

    # Get the todo input if provided
    input_str = update.message.text
    input_str = parse_telegram_input(input_str, None)
    task = " ".join(input_str)   # string without /todo

    if task == '':        # Simply list the content
        with open('todo.txt', 'r') as myfile:
            all_tasks = myfile.read()

        update.message.reply_text(all_tasks, parse_mode=ParseMode.HTML)

    else:         # Append task to the file

        num_lines = sum(1 for line in open('todo.txt'))
        if (num_lines >= 100):
            msg = "Too much work to do. skipped"
        else:
            with open('todo.txt', 'a') as _file:
                _task = "- " + task + "\n"
                _file.write(_task)

            msg = "Added task for review - {}".format(task)

        update.message.reply_text(msg, parse_mode=ParseMode.HTML)


#####################
# Main              #
#####################


def main():
    updater = Updater("589160362:AAHEeNBIeh3m3RA07lANaDHovy874xNFi1g", use_context=True)

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
    dp.add_handler(CommandHandler("todo", todo))


    # Overload command
    dp.add_handler(CommandHandler("s", signal))       # Overloading with /s command
    dp.add_handler(CommandHandler("h", history))      # Overloading with /h command

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
