from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password


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

        user = User.objects.create_user(user_name, email, password, first_name=first_name, last_name=last_name)
        user.save()
        return user


class Login_form(forms.Form):
    user_name = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class Book_search(forms.Form):
    publication_date = forms.DateField(required=False)
    author = forms.CharField(required=False)
    subject_area = forms.CharField(max_length=50)
    title = forms.CharField(required=False)
    shelf_number = forms.CharField(required=False)
