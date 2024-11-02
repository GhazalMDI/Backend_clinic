from django.urls import include, path
from Home import apis

app_name = 'Home'

urlpatterns = [
    path('', apis.HomeAPI.as_view())
]
