from dateutil import parser
import feedparser
from django.core.paginator import Paginator, InvalidPage


class RSSHelper(object):

    @staticmethod
    def get_rss_link(page_no=1):
        _list = []
        rss_link = RSSHelper.get_rss_links()
        paginator = Paginator(rss_link, 1)
        has_next = page_no < paginator.num_pages
        try:
            _list = paginator.page(page_no)[0]
        except InvalidPage:
            return has_next, _list

        return has_next, _list

    @staticmethod
    def get_rss_link_data(link, page_no=1, page_size=20):
        d = feedparser.parse(link)
        _list = []
        paginator = Paginator(d.entries, page_size)
        has_next = page_no < paginator.num_pages
        try:
            d_entries = paginator.page(page_no)
        except InvalidPage:
            return has_next, _list

        for entry in d_entries:
            _list.append(RSSHelper.get_rss_data_from_entry(entry, d.feed["title"]))
        return has_next, _list

    @staticmethod
    def automatePagination_(rss_link_page=1, page_no=1, page_size=20):
        has_next_link, rss_link = RSSHelper.get_rss_link(page_no=rss_link_page)
        final_list = []
        has_next, list = RSSHelper.get_rss_link_data(rss_link['link'], page_no=page_no,
                                                     page_size=page_size)
        if list:
            final_list.append(list)

        if len(list) < page_size and not has_next:
            rss_link_page += 1
            has_next_link, rss_link = RSSHelper.get_rss_link(page_no=rss_link_page)
            has_next, _list = RSSHelper.get_rss_link_data(rss_link['link'], page_no,
                                                          (page_size - len(list)))
            if not _list and has_next_link:
                rss_link_page += 1
                has_next_link, rss_link = RSSHelper.get_rss_link(page_no=rss_link_page)
                has_next, _list = RSSHelper.get_rss_link_data(rss_link['link'], page_no,
                                                              (page_size - len(list)))

            print('inside not next', len(_list), has_next)
            final_list.append(_list)

        if has_next_link:
            has_next = has_next_link

        return has_next, final_list[0]

    @staticmethod
    def get_rss_links():
        rss_list = []
        rss_list.append({'link': 'feed:https://timesofindia.indiatimes.com/rssfeeds/1081479906.cms',
                         'content_type': 'Entertainment'})
        rss_list.append({'link': 'feed:https://thewire.in/rss', 'content_type': 'Entertainment'})
        rss_list.append({'link': 'http://feeds.feedburner.com/ScrollinArticles.rss', 'content_type': 'Entertainment'})
        rss_list.append({'link': 'feed:https://www.livemint.com/rss/politics', 'content_type': 'Entertainment'})
        rss_list.append({'link': 'feed:https://timesofindia.indiatimes.com/rssfeedstopstories.cms',
                         'content_type': 'Entertainment'})
        rss_list.append({'link': 'feed:https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms',
                         'content_type': 'Entertainment'})
        rss_list.append({'link': 'http://feeds.feedburner.com/ScrollinArticles.rss', 'content_type': 'Entertainment'})
        rss_list.append({'link': 'https://indianexpress.com/feed/', 'content_type': 'Entertainment'})
        rss_list.append({'link': 'https://www.thehindu.com/news/national/?service=rss', 'content_type': 'Entertainment'})
        rss_list.append({'link': 'https://www.news18.com/rss/india.xml', 'content_type': 'Entertainment'})
        rss_list.append({'link': 'http://www.firstpost.com/feed/rss', 'content_type': 'Entertainment'})
        rss_list.append({'link': 'feed:https://www.business-standard.com/rss/latest.rss', 'content_type': 'Entertainment'})
        rss_list.append({'link': 'https://prod-qt-images.s3.amazonaws.com/production/thequint/feed.xml',
                         'content_type': 'Entertainment'})
        rss_list.append({'link': 'feed:https://thewire.in/rss', 'content_type': 'Entertainment'})

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
