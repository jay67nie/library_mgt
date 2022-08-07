import datetime

from django.core.mail import send_mail
from django_cron import CronJobBase, Schedule

from .models import borrowed_book


class PenaltyManager(CronJobBase):
    RUN_EVERY_MINS = 60 # every 1 hour

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'The_Library.cron'    # a unique code

    def do(self):
        obj = borrowed_book.objects.all()  # get non-returned books instead
        for x in obj:
            status = x.returned
            return_date = x.due_date
            time_elapse = datetime.date.today() - return_date

            if time_elapse <= 1 and not status:
                send_mail(
                    'Subject here',
                    'Here is the message.',
                    'from@example.com',
                    ['to@example.com'],
                    fail_silently=False,
                )
