from dal import autocomplete
from Doctor.models import MedicalSpecialtyModel, DoctorModel, DetailsMedicalSpecialty


class SpecialtyAuto(autocomplete.Select2QuerySetView):
    print('hiiii')

    def get_queryset(self):
        # def get_queryset(self):
        queryset = MedicalSpecialtyModel.objects.all()
        doctor_id = self.forwarded.get('doctor', None)
        if doctor_id:
            doctor = DoctorModel.objects.filter(id=doctor_id).first()

        # فیلتر بر اساس پارامتر doctor که از URL دریافت شده است
        #     # فرض کنید هر تخصص وابسته به دکتر خاصی است
        #     queryset = queryset.filter(doctor__id=doctor_id)

        return doctor

# queryset = DetailsMedicalSpecialty.objects.all()
#
# # فیلتر بر اساس پارامتر doctor که از URL دریافت شده است
# if doctor_id:
#     # فرض کنید هر تخصص وابسته به دکتر خاصی است
#     queryset = queryset.filter(doctor__id=doctor_id)
#
# return queryset
# print('Inside get_queryset')  # برای بررسی اجرا شدن متد
# if doctor_id := self.forwarded.get('doctor'):
#     print('Doctor ID:', doctor_id)
#     doctor = DoctorModel.objects.filter(id=doctor_id).first()
#     if doctor and doctor.department:
#         print('Doctor department:', doctor.department)
#         return MedicalSpecialtyModel.objects.filter(department__id=doctor.department.id)
# # در صورتی که هیچ داده‌ای پیدا نشد
# print('Returning none')
# return MedicalSpecialtyModel.objects.none()
