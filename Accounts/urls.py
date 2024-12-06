from django.urls import include, path
from Accounts import apis

app_name = 'Accounts'

urlpatterns = [
    path('profile/',apis.ProfileApi.as_view()),
    path('profile/address/',apis.AddressApi.as_view()),
    path('register/',apis.RegisterApi.as_view()),
    path('verify/register/',apis.VerifyRegisterApi.as_view())
]
