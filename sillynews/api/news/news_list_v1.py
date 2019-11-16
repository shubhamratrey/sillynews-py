from api.responses.base import APIResponseBase
from api.decorators.validators import allowed_methods
from helpers.rss_helper import RSSHelper
from django.core.paginator import Paginator, InvalidPage
from constants.error_codes import INVALID_RESOURCE
import feedparser


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
        page_size = self.get_sanitized_int(self.request.GET.get('page_size', self.__page_size__))

        rss_link = RSSHelper.get_rss_links()

        link_paginator = Paginator(rss_link, 1)
        link_has_next = page_no < link_paginator.num_pages
        try:
            page_rss_link = link_paginator.page(page_no)
        except InvalidPage:
            self.set_bad_req('Invalid page no', INVALID_RESOURCE.PAGE)
            return link_has_next, data

        inner_list = []
        for link_data in page_rss_link:
            d = feedparser.parse(link_data['link'])
            paginator = Paginator(d.entries, page_size)
            has_next = page_no < paginator.num_pages
            try:
                d_entries = paginator.page(page_no)
            except InvalidPage:
                self.set_bad_req('Invalid page no', INVALID_RESOURCE.PAGE)
                return has_next, data

            for entry in d_entries:
                inner_list.append(RSSHelper.get_rss_data_from_entry(entry, d.feed["title"]))

        data['data'] = inner_list
        data['has_more'] = has_next
        return data
