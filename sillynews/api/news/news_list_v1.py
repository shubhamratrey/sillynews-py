from api.responses.base import APIResponseBase
from api.decorators.validators import allowed_methods
from helpers.rss_helper import RSSHelper


class NewsListV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')
    __page_size__ = 10

    def __init__(self, **kwargs):
        super(NewsListV1, self).__init__(**kwargs)
        self.allowed_methods = ('GET',)

    @allowed_methods
    def get_or_create_data(self):
        data = {}
        page_no = self.get_sanitized_int(self.request.GET.get('page', 1))
        rss_page_no = self.get_sanitized_int(self.request.GET.get('rss_page', 1))
        page_size = self.get_sanitized_int(self.request.GET.get('page_size', self.__page_size__))
        has_next_rss, link = RSSHelper.get_rss_link(page_no=rss_page_no)
        has_next, list = RSSHelper.get_rss_link_data(link=link['link'], page_no=page_no, page_size=page_size)

        data['data'] = list
        data['has_more'] = has_next
        data['has_more_rss'] = has_next_rss
        return data
