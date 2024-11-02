from django.contrib import admin
from django.urls import path, include

API_URLS = [
    path('', include('Home.urls', namespace='Home')),
    # path('Accounts',include('Accounts.urls',namespace='Accounts'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('API/', include(API_URLS))
]
