from Doctor.models import DoctorModel, CertificateModel
from utils.StandardResponse import get_Response
from django.shortcuts import get_object_or_404


class CertificateHandler:

    @staticmethod
    def delete_certificate(user, pk):
        doctor = DoctorModel.objects.filter(user=user).first()
        if not doctor:
            return get_Response(success=False, message='Doctor not found', status=404)

        certificate = get_object_or_404(CertificateModel, pk=pk, doctor=doctor)
        certificate.delete()
        return get_Response(success=True, message='گواهینامه حذف شد', status=200)
