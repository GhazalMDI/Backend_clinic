from django.urls import path
from Doctor.apis import BookingAPIView

urlpatterns = [
    path('booking/<doctor_id>/<date>/<day>/<time>/<user_id>/', BookingAPIView.as_view()),
]