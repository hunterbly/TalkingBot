import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def main():
    updater = Updater("589160362:AAHEeNBIeh3m3RA07lANaDHovy874xNFi1g", use_context = True)

    # Dispatcher add handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

