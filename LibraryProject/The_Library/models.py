import datetime

from django.contrib.auth import get_user_model
from django.db import models


class book(models.Model):
    publication_date = models.DateField()
    author = models.TextField(max_length=50)
    subject_area = models.CharField(max_length=50)
    title = models.TextField(max_length=50)
    shelf_number = models.CharField(max_length=10)
    borrowed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}: {self.title}"


class borrowed_book(models.Model):
    returned = models.BooleanField()
    book_id = models.ForeignKey(book, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=100, default="")
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    borrow_date = models.DateField()
    borrow_time = models.TimeField(default=datetime.time())
    due_date = models.DateField()
    return_date = models.DateField(null=True)
    penalty_due = models.IntegerField(default=0)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username}"


