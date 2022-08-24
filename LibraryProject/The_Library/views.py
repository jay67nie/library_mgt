import datetime
import threading

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db.models import Q
from django.shortcuts import render, redirect
from verify_email import send_verification_email

from . import notifications
from .forms import SignUp_form, Login_form
from .models import book, borrowed_book
from .notifications import notification_handler

obj = None


def log_in(request):
    if request.method == "GET":
        form = Login_form()
        global obj
        context = {
            "form": form
        }
        if obj:
            obj = None
            messages.success(request, "A verification link has been sent to your email!")
            context["obj"] = True

        # send_mail(
        #     subject='Reminder',
        #     message='Hello, this is to remind you that you have 1 day to return this book. \n'
        #             +'\n\nThank you!',
        #     from_email=None,
        #     recipient_list=['atalamchll7@gmail.com'],
        #     fail_silently=True,
        # )

        return render(request, "login.html", context)


def login_verify(request):
    if request.method == "GET":
        form = Login_form(request.GET)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            # print(request.user)
            user = authenticate(username=user_name, password=password)

            if user is not None and not user.is_superuser:
                login(request, user)
                # print(request.user)
                return redirect('/index/')
            else:
                messages.error(request, "The username or password you entered was incorrect")
                return log_in(request)


def sign_up(request):
    if request.method == 'POST':
        form = SignUp_form(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            re_enter_password = form.cleaned_data['re_enter_password']
            if password == re_enter_password:
                send_verification_email(request, form)
                global obj
                obj = True
                return redirect(log_in)
            else:
                messages.error(request, "The two passwords entered aren't the same")
                return redirect(sign_up)

        else:
            context = {
                "form": form

            }
            return render(request, 'sign_up.html', context)
    else:
        form1 = SignUp_form()

        context = {
            "form": form1

        }
        return render(request, 'sign_up.html', context)


def log_out(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        logout(request)
        # print(request.user)
        return redirect(log_in)
    else:
        redirect("/login/")

        # template=loader.get_template("sign_up.html")
        # HttpResponse(template.render())


# Create your views here.
def search(request):  # function called on first access to search.html
    if request.user.is_authenticated and request.user.is_superuser:
        name = request.GET.get("search")
        try:
            user = get_user_model().objects.get(username__icontains=name)
            obj = borrowed_book.objects.filter(Q(student=user))
        except:
            obj = borrowed_book.objects.all()
            # Using contains to take care of word-spacing.

        my_ctxt = {

            "books": obj,
        }
        # d_title = obj.title
        # my_query = book.objects.filter(title=title)
        print(obj)

        # context = {
        #     "books": my_query
        # }
        return render(request, 'admin/report.html', my_ctxt)


#  DON'T REMOVE THIS INDEX FUNCTION
# def index(request, ctxt=None, *args, **kwargs):
#      my_ctxt = None
#      if ctxt is not None:                          #Checking whether any criteria were passed from forms.
#          title = ctxt.object.title
#          objs = book.objects.filter(title=title)
#          my_ctxt = {
#          "objects": objs
#      }
#      else:
#         objs = list(book.objects.all())
#         my_ctxt = {
#            "objects": objs
#         }
#
#      return render(request, "index.html", my_ctxt)

def index(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        my_books = book.objects.filter(borrowed=False)  # .get(returned=True)
        print(request.user.id)

        context = {
            'books': my_books

        }

        return render(request, 'index.html', context)
    else:
        return redirect("/login/")


def search_result(request):  # Display search results using index.html # Called after submit button is clicked
    # if request.user.is_authenticated:
    #     if request.method == 'GET':  # Checking if the request is GET to bind the user data to a fresh form.
    #         form = Book_search(request.GET)
    #
    #         if form.is_valid():
    #             book = form.cleaned_data['Search']
    #             print(book)
    title = request.GET.get("search")
    obj = book.objects.filter(Q(title__icontains=title),
                              Q(borrowed=False))  # Using contains to take care of word-spacing.

    my_ctxt = {

        "books": obj,
    }
    # d_title = obj.title
    # my_query = book.objects.filter(title=title)
    print(obj)

    # context = {
    #     "books": my_query
    # }
    return render(request, 'index.html', my_ctxt)


#     else:  # Render a 400 code
#
#         return HttpResponseBadRequest("<h1>{{request.method}} is not appropriate for this.")
# else:
#     return redirect("/login/")


def borrowed(request, id):
    if request.user.is_authenticated and not request.user.is_superuser and request.method == 'POST':
        book_id = book.objects.get(id=id)
        books = borrowed_book.objects.filter(Q(student=request.user), Q(returned=False))
        if not book_id.borrowed:
            if len(books) < 3:
                returned = False
                student = request.user
                print(student.id)
                borrow_date = datetime.date.today()
                borrow_time = datetime.datetime.now()
                due_date = borrow_date + datetime.timedelta(weeks=2)
                book_name = book_id.title
                borrowed = not returned
                book_id.borrowed = borrowed
                book_id.save()
                book_id = book.objects.get(id=id)
                my_ctxt = to_return(book_id, request.user)

                transaction = borrowed_book.objects.create(returned=returned, student=student, book_name=book_name,
                                                           borrow_date=borrow_date, borrow_time=borrow_time,
                                                           due_date=due_date,
                                                           book_id=book_id)
                transaction.save()

                # book_id.borrowed = borrowed

                return render(request, "final.html", my_ctxt)
            else:
                messages.error(request, "You have exceeded the maximum number of books to borrow.")
                my_ctxt = to_return(book_id, request.user)
                return render(request, "final.html", my_ctxt)

        else:
            messages.error(request, "This book has already been borrowed.")
            book_id = book.objects.get(id=id)
            my_ctxt = to_return(book_id, request.user)
            return render(request, "final.html", my_ctxt)
    else:
        return redirect("/login/")


def to_return(book, user):
    books = borrowed_book.objects.filter(Q(student=user), Q(returned=False))
    my_ctxt = {
        "books": books,
        "borrowed_book": book
    }
    return my_ctxt


# def auto_report(request):
#     while True:
#         report(request)
#         time.sleep(60)


def report(request):
    if request.user.is_authenticated and request.user.is_superuser:
        notifications_running = notifications.notifications_running
        if not notifications_running:
            print("Notifications started")
            notifications.notifications_running = True
            thread = threading.Thread(target=notification_handler, args=[])
            thread.start()

        obj = borrowed_book.objects.all()  # get non-returned books instead
        for x in obj:
            return_date = x.borrow_date + datetime.timedelta(weeks=2)
            time_elapse = datetime.date.today() - return_date

            if time_elapse.days > 10:
                x.penalty_due = 15000
                x.save()
            elif time_elapse.days > 3:
                x.penalty_due = 5000
                x.save()

        obj = borrowed_book.objects.all().order_by('-borrow_date', '-borrow_time')
        # print(obj)
        # print(request.user.get_full_name)
        my_ctxt = {
            "books": obj
        }

        return render(request, "admin/report.html", my_ctxt)
    else:
        return redirect("/admin/")


def borrow(request, id):
    if request.user.is_authenticated and not request.user.is_superuser:
        obj = book.objects.get(id=id)
        print(obj, id)
        if not obj.borrowed:
            my_ctxt = {
                "book": obj
            }
            return render(request, "borrow.html", my_ctxt)
        else:
            return redirect("/index/")
    else:
        return redirect("/login/")


def terms(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return render(request, "terms.html")


def returned(request, id):
    if request.user.is_authenticated and request.user.is_superuser:

        book = borrowed_book.objects.get(Q(book_id=id), Q(returned=False))
        if request.method == "POST":

            returned = True
            book.returned = returned
            book.book_id.borrowed = not returned
            book.return_date = datetime.date.today()
            book.book_id.save()
            book.save()

            return redirect("/admin/report")
        else:
            return render(request, "admin/returned.html", {"book": book.book_id})


def profile(request):
    if request.user.is_authenticated:
        books = borrowed_book.objects.filter(Q(student=request.user), Q(returned=False))

        for x in books:
            return_date = x.borrow_date + datetime.timedelta(weeks=2)
            time_elapse = datetime.date.today() - return_date

            if time_elapse.days > 10:
                x.penalty_due = 15000
                x.save()
            elif time_elapse.days > 3:
                x.penalty_due = 5000
                x.save()

        # obj = borrowed_book.objects.all()

        context = {
            "books": books

        }
        print(request.user)

        return render(request, "Profile.html", context)
