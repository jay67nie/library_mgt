from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password

# class MinimumLengthValidator :
#     def __init__(self, min_length=8):
#         self.min_length = min_length
#
#     def validate(self, password, user=None):
#         if len(password) < self.min_length:
#             raise forms.ValidationError(_("This password must contain at least %(min_length)d character."), code= 'password_short' , params={'min_length': self.min_length},)
#     def get_help_text (self):
#         return _("Your password must contain at least %(min_length)d characters."
#                  % {'min_length': self.min_length}
#                  )


class SignUp_form(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    user_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    re_enter_password=forms.CharField(max_length=50, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data
        password = data['password']
        validate_password(password)
        return password




    def save(self, commit):
        data = self.cleaned_data
        first_name = data['first_name']
        last_name = data['last_name']
        user_name = data['user_name']
        email = data['email']
        password = data['password']
        # re_enter_password = data['re_enter_password']
        user = User.objects.create_user(user_name, email, password, first_name=first_name, last_name=last_name)
        user.save()
        return user


class Login_form(forms.Form):
    user_name = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


# def clean_data(self):
#     user_name = self.cleaned_data.get("user_name")
#     password = self.cleaned_data.get("password")
#
#     data = Student.objects.filter(user_name=user_name, password=password)
#     if not data:
#         raise forms.ValidationError("Username or password is incorrect")
#
#     return user_name, password


class Book_search(forms.Form):
    publication_date = forms.DateField(required=False)
    author = forms.CharField(required=False)
    subject_area = forms.CharField(max_length=50)
    title = forms.CharField(required=False)
    shelf_number = forms.CharField(required=False)
