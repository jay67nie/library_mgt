from django import forms
from django.contrib.auth.models import User


class SignUp_form(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    user_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    re_enter_password=forms.CharField(max_length=50, widget=forms.PasswordInput)

    # def clean_password(self):
    #     password = self.cleaned_data.get("password")
    #     re_enter_password = self.cleaned_data.get("re_enter_password")
    #
    #     # .objects.filter(password=password,re_enter_password=re_enter_password)
    #
    #     if password != re_enter_password:
    #         raise forms.ValidationError("Two passwords entered aren't the same")
    #     return password, re_enter_password

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
