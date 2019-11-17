from api.responses.base import APIResponseBase
from api.decorators.validators import allowed_methods
from helpers.rss_helper import RSSHelper
from helpers.insta_helper import InstaHelper


class HomeV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')
    __page_size__ = 10

    def __init__(self, **kwargs):
        super(HomeV1, self).__init__(**kwargs)
        self.allowed_methods = ('GET',)

    @allowed_methods
    def get_or_create_data(self):
        data = {}
        items = []
        page_no = self.get_sanitized_int(self.request.GET.get('page', 1))
        rss_page_no = self.get_sanitized_int(self.request.GET.get('rss_page', 1))
        page_size = self.get_sanitized_int(self.request.GET.get('page_size', self.__page_size__))
        has_next_rss, link = RSSHelper.get_rss_link(page_no=rss_page_no)
        has_next, list = RSSHelper.get_rss_link_data(link=link['link'], page_no=page_no, page_size=page_size)

        items.append({
            "type": "information",
            "info": {
                "name": "Shubham Ratrey",
                "quote": "Quote of the day",
                "n_pending_task": "4",
                "n_total_task": "10",
            }
        })

        items.append({
            "type": "tweets",
            "tweets": []
        })

        insta_feed = InstaHelper.get_feed_data()
        items.append({
            "type": "instagram",
            "instagram": insta_feed
        })
        items.append({
            "type": "news",
            "sub_type": "comedy",
            "news": list
        })

        data['items'] = items
        data['has_more'] = has_next
        return data
