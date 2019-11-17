class HomeItemType(object):
    CONTENT_TYPE = 'content-type'
    NEWS_GROUP = 'news_group'
    TWEETS = 'tweets'
    INSTA_FEED = 'insta_feed'
    TASK_FEED = 'task_feed'

    VALID_TYPES = ((CONTENT_TYPE, 'ContentType'), (NEWS_GROUP, 'NewsGroup'), (TWEETS, 'Tweets'), (INSTA_FEED, 'InstaFeed'))


HOME_ITEM_TYPES = HomeItemType()
