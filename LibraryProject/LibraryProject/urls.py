"""LibraryProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from The_Library.views import index, search_result, borrow, report, borrowed, profile, returned, search
from django.conf.urls.static import static
from The_Library.views import log_in, sign_up, login_verify, log_out, terms
from django.contrib import admin
from django.urls import path, include


from LibraryProject import settings

urlpatterns = [
    path('admin/report', report, name='report'),
    path('admin/return/<int:id>', returned, name='return'),
    path('admin/', admin.site.urls),
    path('login/', log_in, name="Login"),
    path('sign_up/', sign_up, name="SignUp"),
    path('verify/', login_verify, name="verify"),
    path('logout/', log_out, name="logout"),
    path('index/', index, name='index'),
    path('', index, name='home'),
    path('admin/report/search/', search, name='search'),
    path('search-result/', search_result, name='search_result'),
    path('borrowed/<int:id>', borrowed, name='borrowed'),
    path('borrow/<int:id>', borrow),
    path('verification/', include('verify_email.urls')),
    path('terms_and_conditions/', terms, name='terms'),
    path('profile/', profile, name= 'profile')

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
