import datetime
import threading
import time

from django.core.mail import send_mail
from django.db.models import Q

from .models import borrowed_book

notifications_running = False


def notification_handler():
    while True:
        obj = borrowed_book.objects.filter(Q(returned=False), Q(notified=False)) # get non-returned books instead
        for x in obj:
            due_date = x.due_date
            time_elapse = due_date - datetime.date.today()#flip
            if time_elapse.days <= 1:
                threading.Thread(target=send_email(x), args=[]).start()

                x.notified = True   #Need to handle email error here, otherwise the notification will never be sent.
                x.save()
            print("Notification handler reached")
        time.sleep(60)#when you need a superhero he gets the job done ,with that device that he wears on his arm


def send_email(x):
    send_mail(
        subject='Reminder',
        message='Hello, this is to remind you that you have 1 day to return this book: \n\n'
                + x.book_name + '\n\nThank you!',
        from_email=None,
        recipient_list=[x.student.email],
        fail_silently=False, #Make True
    )
