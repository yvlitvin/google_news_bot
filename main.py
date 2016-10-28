from telegram import (ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging
import feedparser
import urllib
import sys
sys.stdout = open('out.log', 'w')

flood = 0
def checkFlood(delay):
   while 1:
      global flood
      flood = 0
      time.sleep(60)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)





def search(bot, update):
    user = update.message.from_user
    query = update.message.text
    encoded = urllib.parse.quote_plus(query)
    logger.info("search query of %s: %s" % (user.first_name, query))
    allheadlines = []
    d = feedparser.parse('https://news.google.com.ua/news?ned=uk_ua&hl=ua&q=' + encoded + '&cf=all&output=rss')
    #print(d)
    #print(d.entries)
    newsurls = {'googlenews': 'https://news.google.com.ua/news?ned=ua_ua&hl=ua&q=' + encoded + '&cf=all&output=rss'}
    #print(newsurls)
    # Iterate over the feed urls
    for post in d.entries[:5]:
       # print(post.title + ": " + post.link + "")
        update.message.reply_text(post.title + ": " + post.link + "")

    # Iterate over the allheadlines list and print each headline
    for hl in allheadlines:
        print(hl)
        update.message.reply_text(hl)





def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("278915973:AAHtILE2ry-hFCq940B_-ysIY74jcwPaU4Y")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler([Filters.text], search)],

        states={


            GENDER: [MessageHandler([Filters.text], search)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

