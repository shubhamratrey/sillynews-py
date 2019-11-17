from api.responses.base import APIResponseBase
from api.decorators.validators import allowed_methods
from helpers.rss_helper import RSSHelper
from helpers.insta_helper import InstaHelper
from django.core.paginator import Paginator
from constants import CONTENT_TYPE, HOME_ITEM_TYPES


class HomeV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')
    __page_size__ = 10

    def __init__(self, **kwargs):
        super(HomeV1, self).__init__(**kwargs)
        self.allowed_methods = ('GET',)

    @allowed_methods
    def get_or_create_data(self):
        data = {}
        page_no = self.get_sanitized_int(self.request.GET.get('page', 1))
        items, has_more = self.get_home_items(page=page_no)
        data['items'] = items
        data['has_more'] = has_more
        return data

    def get_page_home_items(self, page_no=1):
        home_items_info = [
            {"type": HOME_ITEM_TYPES.TWEETS},  # tweet_feed
            {"type": HOME_ITEM_TYPES.NEWS_GROUP, "content_type": CONTENT_TYPE.TECHNOLOGY},
            {"type": HOME_ITEM_TYPES.NEWS_GROUP, "content_type": CONTENT_TYPE.POLITICAL},
            {"type": HOME_ITEM_TYPES.INSTA_FEED, "category": CONTENT_TYPE.HOLLYWOOD},  # Insta_feed
            {"type": HOME_ITEM_TYPES.NEWS_GROUP, "content_type": CONTENT_TYPE.ENTERTAINMENT},
            {"type": HOME_ITEM_TYPES.NEWS_GROUP, "content_type": CONTENT_TYPE.TECHNOLOGY},
            {"type": HOME_ITEM_TYPES.NEWS_GROUP, "content_type": CONTENT_TYPE.POLITICAL},
            {"type": HOME_ITEM_TYPES.NEWS_GROUP, "content_type": CONTENT_TYPE.ENTERTAINMENT},
            {"type": HOME_ITEM_TYPES.NEWS_GROUP, "content_type": CONTENT_TYPE.TECHNOLOGY},
            {"type": HOME_ITEM_TYPES.NEWS_GROUP, "content_type": CONTENT_TYPE.POLITICAL},
            {"type": HOME_ITEM_TYPES.NEWS_GROUP, "content_type": CONTENT_TYPE.ENTERTAINMENT},
            {"type": HOME_ITEM_TYPES.INSTA_FEED, "category": CONTENT_TYPE.BOLLYWOOD},  # Insta_feed
        ]
        profile = self.get_profile()
        if profile and page_no == 1:
            home_items_info.insert(0, {"type": HOME_ITEM_TYPES.TASK_FEED})
        home_items_info.insert(0, {"type": HOME_ITEM_TYPES.TASK_FEED})
        home_items, has_more_page = [], False
        paginator = Paginator(home_items_info, 10)
        try:
            home_item_info_page = paginator.page(page_no)
        except:
            return home_items, has_more_page
        else:
            has_more_page = page_no < paginator.num_pages
        for item_info in home_item_info_page:
            home_items.append(item_info)
        return home_items, has_more_page

    def get_home_items(self, page=1):
        items = []
        page_home_items, has_more_page = self.get_page_home_items(page)
        if not page_home_items:
            return items, has_more_page
        for home_item in page_home_items:
            if home_item['type'] == HOME_ITEM_TYPES.TASK_FEED:
                items.append({
                    "type": HOME_ITEM_TYPES.TASK_FEED,
                    "user_info": {
                        "name": "Shubham Ratrey",
                        "quote": "Quote of the day",
                        "n_pending_task": 4,
                        "n_total_task": 10,
                    }
                })
            elif home_item['type'] == HOME_ITEM_TYPES.TWEETS:
                has_more, tweets = False, []
                if tweets:
                    items.append({
                        "type": HOME_ITEM_TYPES.TWEETS,
                        "tweet_feed": tweets
                    })
            elif home_item['type'] == HOME_ITEM_TYPES.INSTA_FEED:
                insta_feed = InstaHelper.get_category_feed_data(home_item['category'])
                if insta_feed:
                    items.append({
                        "type": HOME_ITEM_TYPES.INSTA_FEED,
                        "insta_feed": insta_feed,
                        "category": home_item['category']
                    })

            elif home_item['type'] == HOME_ITEM_TYPES.NEWS_GROUP:
                has_next, group_news = self.get_news_group_data(home_item['content_type'])
                if group_news:
                    items.append({
                        "type": HOME_ITEM_TYPES.NEWS_GROUP,
                        "content_type": home_item['content_type'],
                        "news": group_news,
                        "has_more": has_next,
                    })

        return items, has_more_page

    def get_news_group_data(self, _filter):
        has_next_rss, link = RSSHelper.get_rss_link(page_no=1, _filter=_filter)
        has_next, group_news = RSSHelper.get_rss_link_data(link=link['link'], page_no=1, page_size=10)
        return has_next, group_news
