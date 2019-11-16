from django.urls import include, re_path

urlpatterns = [
    re_path(r'^v(?P<_v>[0-9.]+)/', include('api.urls'))
]
