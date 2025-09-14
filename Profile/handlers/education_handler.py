from Doctor.models import DoctorModel, EducationDetailsModel
from utils.StandardResponse import get_Response


class EducationHandler:

    @staticmethod
    def delete_education(user, pk):
        doctor = DoctorModel.objects.filter(user=user).first()
        if not doctor:
            return get_Response(success=False, message='Doctor not found', status=404)
        education = EducationDetailsModel.objects.filter(pk=pk, doctor=doctor).first()
        if not education:
            return get_Response(success=False, message='رکورد تحصیلات یافت نشد', status=404)

        education.delete()
        return get_Response(success=True, message='رکورد تحصیلات حذف شد', status=200)
