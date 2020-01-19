import logging
from functools import wraps
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction

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
    print(update)
    print(context)
    update.message.reply_text('Test!')
    # chat_id = bot.get_updates()[-1].message.chat_id

@typing
def testing(update, context):
    """Send a message when the command /testing is issued."""
    update.message.reply_text('Testing!')

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

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
    
    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

