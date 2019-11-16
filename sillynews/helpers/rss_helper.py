from dateutil import parser


class RSSHelper(object):

    @staticmethod
    def get_rss_links():
        rss_list = []
        rss_list.append({'link': 'feed:https://timesofindia.indiatimes.com/rssfeeds/1081479906.cms',
                         'content_type': 'Entertainment'})
        rss_list.append({'link': 'feed:https://thewire.in/rss', 'content_type': 'Entertainment'})
        # rss_list.append('feed:https://thewire.in/rss')
        # rss_list.append('http://feeds.feedburner.com/ScrollinArticles.rss')
        # rss_list.append('feed:https://www.livemint.com/rss/politics')
        # rss_list.append('feed:https://timesofindia.indiatimes.com/rssfeedstopstories.cms')
        # rss_list.append('feed:https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms')
        # rss_list.append('http://feeds.feedburner.com/ndtvnews-top-stories')
        # rss_list.append('http://feeds.feedburner.com/ScrollinArticles.rss')
        # rss_list.append('https://indianexpress.com/feed/')
        # rss_list.append('https://www.thehindu.com/news/national/?service=rss')
        # rss_list.append('https://www.news18.com/rss/india.xml')
        # # rss_list.append('http://www.firstpost.com/feed/rss') taking too long to load
        # rss_list.append('feed:https://www.business-standard.com/rss/latest.rss')
        # rss_list.append('https://prod-qt-images.s3.amazonaws.com/production/thequint/feed.xml')
        # rss_list.append('feed:https://thewire.in/rss')

        return rss_list

    @staticmethod
    def get_rss_data_from_entry(entry, headerSource):
        # print(entry.keys())
        data = dict()

        # Title & Description
        if entry.has_key('title') and len(entry.title) != 0:
            data['title'] = entry.title
        if entry.has_key('summary') and len(entry.summary) != 0:
            data['description'] = RSSHelper.remove_html_tags(entry.summary)

        # Links
        if entry.has_key('link') and len(entry.link) != 0:
            data['link'] = entry.link

        # Images
        images = dict()
        if entry.has_key('storyimage') and len(entry.storyimage) != 0:
            images['thumbnail_url'] = entry.storyimage
        elif entry.has_key('media_thumbnail') and entry.media_thumbnail and entry.media_thumbnail[0]['url'] != 0:
            images['thumbnail_url'] = entry.media_thumbnail[0]['url']

        if entry.has_key('fullimage') and len(entry.fullimage) != 0:
            images['original_image'] = entry.fullimage

        if len(images) != 0:
            data['images'] = images

        # Source
        if entry.has_key('source') and entry.source.has_key('title') and len(entry.source['title']) != 0:
            data['source'] = entry.source['title']
        elif entry.has_key('author') and len(entry.author) != 0:
            data['source'] = entry.author
        elif len(headerSource) > 0:
            data['source'] = headerSource

        # Date & Time
        if entry.has_key('published') and len(entry.published) != 0:
            data['published_date'] = parser.parse(entry.published).isoformat()

        return data

    @staticmethod
    def remove_html_tags(text):
        """Remove html tags from a string"""
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
