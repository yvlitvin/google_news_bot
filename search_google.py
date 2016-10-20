import feedparser
import urllib
import logging

logging.basicConfig(level=logging.DEBUG)


query = 'міст патона'
encoded = urllib.parse.quote_plus(query)
# Function to fetch the rss feed and return the parsed RSS
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

newsurls = {'googlenews': 'https://news.google.com.ua/news?ned=ua_ua&hl=ua&q='+encoded+'&cf=all&output=rss'}
print(newsurls)
# Iterate over the feed urls
for key, url in newsurls.items():
    # Call getHeadlines() and combine the returned headlines with allheadlines
    allheadlines.extend(getHeadlines(url))

# Iterate over the allheadlines list and print each headline
for hl in allheadlines:
    print(hl)


    # end of code