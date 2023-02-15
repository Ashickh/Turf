
from asyncio.log import logger
import email
from email import message

from celery import Celery

from celery import shared_task

# from celery.utils.log import get_task_logger

from django.conf import settings

from django.core.mail import send_mail

from Turf.celery import app

from .models import Booking

import datetime

from datetime import date, timedelta



@shared_task
def send_issue_mail(email, message):
    logger.info("inside send mail task")

    send_mail(
        subject = 'Turf Booked Successfully',
        message = message,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = [email],
        fail_silently = False,
    ) 

    print("Turf Booking mail has been sent")
    return "Done"