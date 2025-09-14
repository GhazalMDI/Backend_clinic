from django.urls import include, path
from Accounts import apis

app_name = 'Accounts'

urlpatterns = [
   
    path('register/', apis.RegisterApi.as_view()),
    path('verify/register/', apis.VerifyRegisterApi.as_view()),
    path('logout/', apis.LogoutApi.as_view()),
    path('GoogleLogin/', apis.GoogleLoginApi.as_view()),
]
