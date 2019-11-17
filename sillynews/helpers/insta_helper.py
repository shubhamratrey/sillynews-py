import random
from django.core.paginator import Paginator, InvalidPage
from helpers.scrapper_helper import ScrapperHelper


class InstaHelper(object):

    @staticmethod
    def get_instagram_profile_link_from_username(username):
        return format('https://www.instagram.com/%s/?hl=en' % username)

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
            random.shuffle(posts)
            data.append(posts[0])
            data.append(posts[1])
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
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    data = dict()
                    data['thumbnail_src'] = node['thumbnail_src']
                    data['display_url'] = node['display_url']
                    if node['edge_media_to_caption'] and len(node['edge_media_to_caption']['edges']) > 0:
                        data['caption'] = node['edge_media_to_caption']['edges'][0]['node']['text']
                    data['username'] = node['owner']['username']
                    data['n_likes'] = node['edge_liked_by']['count']
                    data['n_comments'] = node['edge_media_to_comment']['count']
                    data['link'] = profile_url
                    results.append(data)
        return results
