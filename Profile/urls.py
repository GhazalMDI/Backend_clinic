from django.urls import path
from Profile import apis


urlpatterns = [
    path('profile/', apis.ProfileApi.as_view()),
    path('profile/EditDelete/<int:pk>',apis.ProfileEditDeleteApi.as_view()),
    path('profile/address/', apis.AddressApi.as_view()),
]
