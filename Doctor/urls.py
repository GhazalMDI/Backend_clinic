from django.urls import path
from Doctor import apis


urlpatterns = [
    path('booking/<doctor_id>/<date>/<day>/<time>/<user_id>/', apis.BookingAPIView.as_view()),
]