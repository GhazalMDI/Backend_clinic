from Doctor.models import DoctorModel
from utils.StandardResponse import get_Response
from utils.imageCompress import compress_image


class DoctorHandler:

    @staticmethod
    def update_image(user, image):
        if not user or not user.is_authenticated:
            return get_Response(success=False, message='Unauthorized', status=401)

        doctor = DoctorModel.objects.filter(user=user).first()
        if not doctor:
            return get_Response(success=False, message='Doctor not found', status=404)

        if not image:
            return get_Response(success=False, message='No image uploaded', status=400)

        max_upload_size = 10 * 1024 * 1024  # 10MB
        max_size = 150 * 1024  # 150KB

        if image.size > max_upload_size:
            return get_Response(success=False, message='Image larger than 10MB', status=400)

        if image.size > max_size:
            image = compress_image(image)

        if doctor.image:
            doctor.image.delete()

        doctor.image = image
        doctor.save()

        return get_Response(success=True, message='تصویر پروفایل بروزرسانی شد',
                            data={'image_url': doctor.image.url}, status=200)
