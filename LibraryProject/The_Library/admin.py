from django.contrib import admin
from .models import book, borrowed_book


@admin.register(book)
class bookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "shelf_number")


# @admin.register(borrowed_book)
@admin.display(description="Book ID")
def book_idx(obj):
    return obj.book_id.id

@admin.display(description="Student ID")
def studentx(obj):
    return obj.student.id


class borrowed_bookAdmin(admin.ModelAdmin):
    list_display = (studentx, book_idx, "borrow_date", "due_date", "return_date", "returned", "penalty_due")


admin.site.register(borrowed_book, borrowed_bookAdmin)
# Register your models here.
