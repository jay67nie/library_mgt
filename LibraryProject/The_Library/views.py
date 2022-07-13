import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect

from .forms import Book_search
from .forms import SignUp_form, Login_form
from .models import book, borrowed_book


def log_in(request):
    if request.method == "GET":
        form = Login_form()
        context = {
            "form": form
        }
        print("__init__")
        return render(request, "login.html", context)


def login_verify(request):
    if request.method == "GET":
        form = Login_form(request.GET)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            # print(request.user)
            user = authenticate(username=user_name, password=password)

            if user is not None:
                login(request, user)
                # print(request.user)
                return redirect('/index/')
            else:
                return log_in(request)


def sign_up(request):
    if request.method == 'POST':
        form = SignUp_form(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user_name = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(form.cleaned_data)

            # object =Student.objects.create(first_name=first_name,last_name=last_name,user_name=user_name,email=email,password=password)
            # object.save()
            user = User.objects.create_user(user_name, email, password, first_name=first_name, last_name=last_name)
            user.save()

            return redirect(log_in)


    else:
        form1 = SignUp_form()

        context = {
            "form": form1

        }
        return render(request, 'sign_up.html', context)


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        # print(request.user)
        return redirect(log_in)
    else:
        redirect("/login/")

        # template=loader.get_template("sign_up.html")
        # HttpResponse(template.render())


# Create your views here.
def search(request):  # function called on first access to search.html
    if request.user.is_authenticated:
        if request.method == 'GET':
            my_form = Book_search()
            my_ctxt = {
                "form": my_form
            }
            return render(request, "search.html", my_ctxt)
        else:  # Render a 400 code

            return HttpResponseBadRequest("<h1>{{request.method}} is not appropriate for this.")
    else:
        return redirect("/login/")


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
    if request.user.is_authenticated:
        my_books = book.objects.filter(borrowed=False)   #.get(returned=True)
        print(request.user.id)

        context = {
            'books': my_books

        }

        return render(request, 'index.html', context)
    else:
        return redirect("/login/")


def search_result(request):  # Display search results using index.html # Called after submit button is clicked
    if request.user.is_authenticated:
        if request.method == 'GET':  # Checking if the request is GET to bind the user data to a fresh form.
            form = Book_search(request.GET)

            if form.is_valid():
                subject_area = form.cleaned_data['subject_area']
                print(subject_area)
                obj = list(book.objects.filter(
                    subject_area__icontains=subject_area))  # Using contains to take care of word-spacing.

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



        else:  # Render a 400 code

            return HttpResponseBadRequest("<h1>{{request.method}} is not appropriate for this.")
    else:
        return redirect("/login/")


def borrowed(request, id):
    if request.user.is_authenticated:
        book_id = book.objects.get(id=id)
        returned = False
        student = request.user.get_full_name()  # student = request.user
        borrow_date = datetime.date.today()
        book_name = book_id.title
        borrowed = not returned
        book_id.borrowed = borrowed
        book_id.save()
        book_id = book.objects.get(id=id)


        transaction = borrowed_book.objects.create(returned=returned, student=student, book_name=book_name,
                                                   borrow_date=borrow_date,
                                                   book_id=book_id)
        transaction.save()

        book_id.borrowed = borrowed

        return render(request, "final.html")
    else:
        return redirect("/login/")


def report(request):
    if request.user.is_authenticated:
        obj = borrowed_book.objects.all() #get non-returned books instead
        for x in obj:
            return_date = x.borrow_date + datetime.timedelta(weeks=2)
            time_elapse = datetime.date.today() - return_date

            if time_elapse.days > 10:
                x.penalty_due = 15000
                x.save()
            elif time_elapse.days > 3:
                x.penalty_due = 5000
                x.save()

        obj = borrowed_book.objects.all()
        # print(obj)
        # print(request.user.get_full_name)
        my_ctxt = {
            "books": obj
        }

        return render(request, "admin/report.html", my_ctxt)
    else:
        return redirect("/login/")


def borrow(request, id):
    if request.user.is_authenticated:
        obj = book.objects.get(id=id)
        print(obj, id)
        my_ctxt = {
            "book": obj
        }
        return render(request, "borrow.html", my_ctxt)
    else:
        return redirect("/login/")
