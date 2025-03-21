from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

API_URLS = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('', include('Home.urls', namespace='Home')),
    path('Doctor/',include('Doctor.urls')),
    path('Accounts/',include('Accounts.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('API/', include(API_URLS))
]
