from Doctor.models import DoctorModel, WorkingHourModel
from utils.StandardResponse import get_Response


class WorkingHourHandler:

    @staticmethod
    def delete_workinghour(user, pk):
        doctor = DoctorModel.objects.filter(user=user).first()
        if not doctor:
            return get_Response(success=False, message='Doctor not found', status=404)

        workhour = WorkingHourModel.objects.filter(pk=pk, doctor=doctor).first()
        if not workhour:
            return get_Response(success=False, message='رکورد یافت نشد', status=404)

        workhour.delete()
        return get_Response(success=True, message='ساعت کاری حذف شد', status=200)
