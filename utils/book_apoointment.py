from datetime import timedelta, datetime
from django.utils.timezone import now
from django.core.exceptions import ValidationError

from Doctor.models import AppointmentModel


def get_available_slots(doctor, date, patient, time):
    if date <= now().date():
        raise ValidationError('رزور وقت گذشته است')

    selected_day = date.strftime('%A').upper()
    working_hours = doctor.doctor_working_hours.filter(day=selected_day).exists()
    if not working_hours:
        raise ValidationError('در این روز، دکتر در مجموعه حضور ندارد')

    if not any(work.start_time <= time < work.end_time for work in working_hours):
        raise ValidationError('این زمان در بازه ی حضور نیست.')

    if overlapping_appointments := AppointmentModel.objects.filter(doctor__exact=doctor, time=time, date=date).exists():
        raise ValidationError('این بازه ی زمانی پر است')

    else:
        overlapping_appointments.objects.create(doctor=doctor, patient=patient, time=time, date=date)

    return overlapping_appointments
