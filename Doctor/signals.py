# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from Doctor.models import AppointmentModel
# from utils.sms import send_message,send_code

# @receiver(post_save, sender=AppointmentModel)
# def send_qr_sms(sender, instance, created, **kwargs):
    
#     print('sssssssssssssssssssssssssssssss')
#     if created:
#         frontend_base_url = "http://localhost:4200/"  # آدرس دامنه‌ی فرانت شما
#         qr_url = f"{frontend_base_url}/appointment/qr/{self.qr_token}"
#         print('hi signals')
        
        
#         send_code(
#             phone=instance.patent.phone_number,  # به جای شماره‌ی ثابت، از فیلد مدل استفاده کن
#             code=f'''سلام {instance.patent.first_name} {instance.patent.last_name}،
# نوبت شما با دکتر {instance.doctor.last_name} در تاریخ {instance.date} ثبت شد.
# برای مشاهده جزئیات نوبت به لینک زیر مراجعه فرمایید:
# {qr_url}'''
#         )



