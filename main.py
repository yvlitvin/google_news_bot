from telegram import (ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging
import feedparser
import urllib


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)


def start(bot, update):
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return GENDER


def search(bot, update):
    user = update.message.from_user
    query = update.message.text
    encoded = urllib.parse.quote_plus(query)
    logger.info("Gender of %s: %s" % (user.first_name, query))

    update.message.reply_text('I see! Please send me a photo of yourself, '
                              'so I know what you look like, or send /skip if you don\'t want to.')

    def parseRSS(rss_url):
        return feedparser.parse(rss_url)

    # Function grabs the rss feed headlines (titles) and returns them as a list
    def getHeadlines(rss_url):
        headlines = []

        feed = parseRSS(rss_url)
        for newsitem in feed['items']:
            headlines.append(newsitem['title'])
            headlines.append(newsitem['link'])

        return headlines

    # A list to hold all headlines
    allheadlines = []

    # List of RSS feeds that we will fetch and combine

    newsurls = {'googlenews': 'https://news.google.com.ua/news?ned=ua_ua&hl=ua&q=' + encoded + '&cf=all&output=rss'}
    print(newsurls)
    # Iterate over the feed urls
    for key, url in newsurls.items():
        # Call getHeadlines() and combine the returned headlines with allheadlines
        allheadlines.extend(getHeadlines(url))

    # Iterate over the allheadlines list and print each headline
    for hl in allheadlines:
        print(hl)


    return PHOTO



def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={


            GENDER: [MessageHandler([Filters.text], search())]
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

