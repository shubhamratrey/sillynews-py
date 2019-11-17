import random
from django.core.paginator import Paginator, InvalidPage
from helpers.insta_scrapper import InstaScraper


class InstaHelper(object):

    @staticmethod
    def account_links():
        account_list = [{'insta_id': 'lilireinhart', 'content_type': 'Entertainment'},
                        {'insta_id': 'andreeacristina', 'content_type': 'Entertainment'},
                        {'insta_id': 'manushi_chhillar', 'content_type': 'Entertainment'},
                        {'insta_id': 'iss', 'content_type': 'Entertainment'},
                        {'insta_id': 'spacex', 'content_type': 'Entertainment'},
                        {'insta_id': 'kuku_fm', 'content_type': 'Entertainment'},
                        {'insta_id': 'sonaakshiraaj', 'content_type': 'Entertainment'},
                        {'insta_id': 'aliaabhatt', 'content_type': 'Entertainment'},
                        {'insta_id': 'barkhasingh0308', 'content_type': 'Entertainment'},
                        {'insta_id': 'tarasutaria', 'content_type': 'Entertainment'},
                        {'insta_id': 'aditiraohydari', 'content_type': 'Entertainment'},
                        {'insta_id': 'jeffbezos', 'content_type': 'Entertainment'},
                        {'insta_id': 'sundarpichai', 'content_type': 'Entertainment'},
                        {'insta_id': 'kaajal9', 'content_type': 'Entertainment'},
                        {'insta_id': 'amberheard', 'content_type': 'Entertainment'},
                        {'insta_id': 'sarya12', 'content_type': 'Entertainment'},
                        ]

        for account in account_list:
            account['link'] = format('https://www.instagram.com/%s/?hl=en' % account['insta_id'])

        random.shuffle(account_list)
        return account_list

    @staticmethod
    def get_account_link(page_no=1):
        _list = []
        rss_link = InstaHelper.account_links()
        rss_link = random.shuffle(rss_link)
        paginator = Paginator(rss_link, 2)
        has_next = page_no < paginator.num_pages
        try:
            _list = paginator.page(page_no)[0]
        except InvalidPage:
            return has_next, _list

        return has_next, _list

    @staticmethod
    def get_feed_data():
        data = []
        rank = 0
        for account in InstaHelper.account_links()[:5]:
            rank += 1
            print(rank)
            posts = InstaScraper().profile_page_recent_posts(account['link'])
            random.shuffle(posts)
            data.append(posts[0])
            data.append(posts[1])
        random.shuffle(data)
        return data
