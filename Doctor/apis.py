from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from Accounts.models import User
from Doctor.serializers import *
from utils.book_apoointment import get_available_slots
from utils.StandardResponse import get_Response


class BookingAPIView(APIView):

    def get(self, request, doctor_id, date, time, user_id):
        if request.user and request.user.is_authenticated:
            doctor = DoctorModel.objects.filter(pk=doctor_id).first()
            patient = User.objects.filter(pk=user_id, is_doctor=False).first()
            try:
                appointment = get_available_slots(doctor, date=date, patient=patient, time=time)
                asrz = AppointmentSerializers(appointment)

                return Response(
                    {
                        "success": True,
                        "message": 'رزرو نوبت انجام شد',
                        "data": asrz.data,
                    }, status=201,
                )

            except ValidationError as e:
                return Response({"success": False, "message": str(e)}, status=400)


class PatientListAPIView(APIView):
    def get(self, request):
        appointments = AppointmentModel.objects.all()
        if request.user and request.user.is_authenticated:
            if doctor := DoctorModel.objects.filter(user__phone_number=request.user).first():
                appointment = appointments.filter(doctor_id=doctor)
                asrz = AppointmentSerializers(appointment,many=True)

                return get_Response(
                    success=True,
                    status=200,
                    data=asrz.data,
                    message='لیست نوبت های شما'
                )

            if patient := User.objects.filter(pk=request.user, is_doctor=False).first():
                appointment = appointments.filter(patient_id=patient)
                asrz = AppointmentSerializers(appointment, many=True)
                return get_Response(
                    success=True,
                    status=200,
                    data=asrz.data,
                    message='نوبت های اخذ شده'
                )
        return get_Response(
            success=False,
            status=401,
            message='وارد حساب کاربری خود شوید'
        )


