import feedparser

def feed_parser():
    NewsFeed = {'РосРеестр': 'https://rosreestr.ru/site/rss/',
                            'Федеральная Налоговая Служба': 'https://www.nalog.ru/rn62/rss/'}
    message = dict()
    for key in NewsFeed.keys():
        current_news = feedparser.parse(NewsFeed[key]).entries[0]
        message[key] = current_news.title + '\n' + current_news.link
    return message