import datetime

from django.core.mail import send_mail
from django_cron import CronJobBase, Schedule

from .models import borrowed_book


class Penalty(CronJobBase):
    RUN_EVERY_MINS = 5 # every 1 hour
    RETRY_AFTER_FAILURE_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'Penalty'  # a unique code

    def do(self):
        obj = borrowed_book.objects.filter(returned=False)  # get non-returned books instead
        for x in obj:
            notified = x.notified
            return_date = x.due_date
            time_elapse = datetime.date.today() - return_date

            if time_elapse.weeks <= 2 and not notified:
                send_mail(
                    subject='Reminder',
                    message='Hello, this is to remind you that you have 1 day to return this book. \n'
                            + x.book_name + '\n\nThank you!',
                    from_email=None,
                    recipient_list=[x.student.email],
                    fail_silently=False,
                )

                x.notified = True
                x.save()
