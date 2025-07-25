from django.db.models.signals import post_save
from django.dispatch import receiver
from Doctor.models import AppointmentModel
from utils.sms import send_message

@receiver(post_save,sender=AppointmentModel)
def send_qr_sms(sender,instance,created,**kwargs):
    if created:
        send_message(
            phone='09157890381',
            message=f'''سلام {instance.patent.first_name} {instance.patent.last_name} نوبت شما با {instance.doctor.last_name} 
             ثبت شد {instance.date} در تاریخ
               برای مشاهده به لینک زیر مراجعه نمایید,{instance.get_qr_url()} '''

        )



