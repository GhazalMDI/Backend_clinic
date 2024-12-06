from django.contrib import admin
from django.urls import path, include

API_URLS = [
    path('', include('Home.urls', namespace='Home')),
    path('Doctor/',include('Doctor.urls')),
    path('Accounts/',include('Accounts.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('API/', include(API_URLS))
]
