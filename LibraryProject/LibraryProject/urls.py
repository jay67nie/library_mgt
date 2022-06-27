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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin, staticfiles
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from The_Library.views import log_in,sign_up,login_verify,log_out
from The_Library.views import index, search, search_result, borrow, terms
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/report', TemplateView.as_view(template_name='admin/report.html'), name='report'),
    path('admin/', admin.site.urls),
    path('login/',log_in,name="Login"),
    path('sign_up/',sign_up,name="SignUp"),
    path('verify/',login_verify,name="verify"),
    path('logout',log_out,name="logout"),
    path('index/',index,name='index'),
    path('search/',search,name='search'),
    path('search-result/', search_result, name='search_result'),
    path('terms/<int:id>', terms),
    path('borrow/<int:id>', borrow),

]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_FILES)