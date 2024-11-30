from datetime import timedelta, datetime
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db import transaction

from Doctor.models import AppointmentModel,DoctorModel


def get_available_slots(doctor, date, patient, time):
    
        day=date.weekday()
        print(day)
        if date <= now().date():
            raise ValidationError('رزور وقت گذشته است')

        working_hours = doctor.doctor_working_hours.filter(day=day)
        if not working_hours:
            raise ValidationError('در این روز، دکتر در مجموعه حضور ندارد')
        
        for work in working_hours:
            if not (work.start_time) <= time < (work.end_time):
                raise ValidationError('این زمان در بازه ی حضور نیست.')
            
        appointment_time = datetime.strptime(str(time), "%H:%M:%S").time()
        # appointment_datetime = datetime.combine(datetime.today(), appointment_time)
        start_time = (datetime.combine(datetime.today(), appointment_time) - timedelta(minutes=7)).time()  # 15 دقیقه قبل
        end_time = (datetime.combine(datetime.today(), appointment_time) + timedelta(minutes=7)).time()  # 15 دقیقه بعد
        print(start_time)
        print(end_time)
        
        with transaction.atomic():
            if overlapping_appointments := AppointmentModel.objects.filter(doctor__id=doctor.id, date=date,time__gte=start_time,time__lt=end_time):
                    raise ValidationError('این بازه زمانی پر است یا با رزروی دیگر تداخل دارد.')
            elif not overlapping_appointments:
                    overlapping_appointments=AppointmentModel.objects.create(doctor=doctor, patient=patient, time=time, date=date)
        return overlapping_appointments

