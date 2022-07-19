from django import forms


class SignUp_form(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    user_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    re_enter_password=forms.CharField(max_length=50, widget=forms.PasswordInput)

    def clean_password(self):
        password=self.cleaned_data.get("password")
        re_enter_password=self.cleaned_data.get("re_enter_password")

        # .objects.filter(password=password,re_enter_password=re_enter_password)

        if password != re_enter_password:
            raise forms.ValidationError("Two passwords entered aren't the same")
        return password,re_enter_password

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
