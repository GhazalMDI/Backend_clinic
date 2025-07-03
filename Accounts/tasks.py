from celery import shared_task

@shared_task
def say_hello():
    print("hello redis!")