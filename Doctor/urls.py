from django.urls import path
from Doctor.apis import SpecialtyAuto

urlpatterns = [
    path('specialty-autocomplete/', SpecialtyAuto.as_view(), name='specialty-autocomplete'),
]