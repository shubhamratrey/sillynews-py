from django.urls import include, re_path

from .users import urls as users_urls
from .news import urls as news_urls
from .home import urls as home_urls

urlpatterns = [
    re_path('^users/', include(users_urls)),
    re_path('^news/', include(news_urls)),
    re_path('^home/', include(home_urls)),
]
