from django.urls import include, path
from Accounts import apis

app_name = 'Accounts'

urlpatterns = [
    path('profile/address/',apis.AddressApi.as_view())
    # path('register/',include())
]
