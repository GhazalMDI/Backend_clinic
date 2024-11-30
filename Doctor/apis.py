from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError


from Accounts.models import User
from Doctor.serializers import *
from utils.book_apoointment import get_available_slots
from utils.StandardResponse import get_Response


class BookingAPIView(APIView):

    def get(self, request, doctor_id, date, time, user_id):
        doctor = DoctorModel.objects.filter(pk=doctor_id).first()
        patient = User.object.filter(pk=user_id, is_doctor=False).first()
        try:
            appointment  = get_available_slots(doctor, date=date, patient=patient, time=time)
            asrz = AppointmentSerializers(appointment)
            
            return Response(
                {
                    "success":True,
                    "message":'رزرو نوبت انجام شد',
                    "data": asrz.data,
                }, status=201,
            )
            
        except ValidationError as e:
             return Response({"success": False, "message": str(e)}, status=400)
            
