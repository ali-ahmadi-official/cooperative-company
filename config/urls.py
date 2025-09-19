"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from django.shortcuts import redirect
from django.contrib.auth import logout

def admin_logout(request):
    logout(request)
    return redirect('/admin/login/')

def people_logout(request):
    logout(request)
    return redirect('/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('page.urls')),
    path('logout/', people_logout, name='people_logout'),
    path('admin/logout/', admin_logout, name='admin_logout'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

admin.site.index_title = "به پنل مدیریت خوش آمدید"
