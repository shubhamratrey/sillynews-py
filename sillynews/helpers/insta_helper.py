import random
from django.core.paginator import Paginator, InvalidPage
from helpers.scrapper_helper import ScrapperHelper
from constants import CONTENT_TYPE


class InstaHelper(object):

    @staticmethod
    def get_instagram_profile_link_from_username(username):
        return format('https://www.instagram.com/%s/?hl=en' % username)

    @staticmethod
    def account_links():
        account_list = [{'insta_id': 'lilireinhart', 'category': CONTENT_TYPE.ENTERTAINMENT},
                        {'insta_id': 'andreeacristina', 'category': CONTENT_TYPE.ENTERTAINMENT},
                        {'insta_id': 'manushi_chhillar', 'category': CONTENT_TYPE.ENTERTAINMENT},
                        {'insta_id': 'iss', 'category': CONTENT_TYPE.SPACE},
                        {'insta_id': 'spacex', 'category': CONTENT_TYPE.SPACE},
                        {'insta_id': 'kuku_fm', 'category': CONTENT_TYPE.ENTERTAINMENT},
                        {'insta_id': 'sonaakshiraaj', 'category': CONTENT_TYPE.BOLLYWOOD},
                        {'insta_id': 'aliaabhatt', 'category': CONTENT_TYPE.BOLLYWOOD},
                        {'insta_id': 'barkhasingh0308', 'category': CONTENT_TYPE.ENTERTAINMENT},
                        {'insta_id': 'tarasutaria', 'category': CONTENT_TYPE.BOLLYWOOD},
                        {'insta_id': 'aditiraohydari', 'category': CONTENT_TYPE.BOLLYWOOD},
                        {'insta_id': 'jeffbezos', 'category': CONTENT_TYPE.TECHNOLOGY},
                        {'insta_id': 'sundarpichai', 'category': CONTENT_TYPE.TECHNOLOGY},
                        {'insta_id': 'kaajal9', 'category': CONTENT_TYPE.BOLLYWOOD},
                        {'insta_id': 'amberheard', 'category': CONTENT_TYPE.HOLLYWOOD},
                        {'insta_id': 'sarya12', 'category': CONTENT_TYPE.ENTERTAINMENT},
                        ]

        for account in account_list:
            account['link'] = InstaHelper.get_instagram_profile_link_from_username(account['insta_id'])

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
        for account in InstaHelper.account_links()[:5]:
            posts = InstaHelper.profile_page_recent_posts(account['link'])
            if posts:
                random.shuffle(posts)
                data.append(posts[0])
                data.append(posts[1])
        random.shuffle(data)
        return data

    @staticmethod
    def get_category_feed_data(category):
        data = []
        account_list = []
        accounts = InstaHelper.account_links()
        for account in accounts:
            if account['category'] in category:
                account_list.append(account)
        random.shuffle(account_list)
        for account in account_list:
            posts = InstaHelper.profile_page_recent_posts(account['link'])
            if posts:
                random.shuffle(posts)
                data.append(posts[random.choice([1, 3, 5, 7, 9])])
                data.append(posts[random.choice([2, 4, 6, 8, 10])])
        random.shuffle(data)
        return data

    @staticmethod
    def profile_page_metrics(profile_url):
        results = {}
        try:
            response = ScrapperHelper.get_response_from_url(profile_url)
            json_data = ScrapperHelper.extract_json_data_from_html(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                if key != 'edge_owner_to_timeline_media':
                    if value and isinstance(value, dict):
                        value = value['count']
                        results[key] = value
                    elif value:
                        results[key] = value
        return results

    @staticmethod
    def profile_page_recent_posts(profile_url):
        results = []

        try:
            response = ScrapperHelper.get_response_from_url(profile_url)
            json_data = ScrapperHelper.extract_json_data_from_html(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'][
                "edges"]
            user_metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    data = dict()
                    data['id'] = node['id']
                    data['thumbnail_src'] = node['thumbnail_src']
                    data['display_url'] = node['display_url']
                    if node['edge_media_to_caption'] and len(node['edge_media_to_caption']['edges']) > 0:
                        data['caption'] = node['edge_media_to_caption']['edges'][0]['node']['text']
                    data['n_likes'] = node['edge_liked_by']['count']
                    data['n_comments'] = node['edge_media_to_comment']['count']
                    if node['location']:
                        data['location'] = node['location']['name']
                    profile = dict()
                    profile['username'] = node['owner']['username']
                    profile['profile_pic_url'] = user_metrics['profile_pic_url']
                    profile['profile_pic_url_hd'] = user_metrics['profile_pic_url_hd']
                    profile['profile_link'] = profile_url
                    data['profile'] = profile
                    results.append(data)
        return results
