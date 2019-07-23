"""django_tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from codeView.views import codeView,bad_request,server_error
from codeView.views import getcode,getAllStudent,getProblemList,analysisView,mutiCodeView
from django.conf.urls import handler400, handler403, handler404, handler500



urlpatterns = [
    path('codeview/', codeView),
    path('codeview/Analysis/', analysisView),
    path('codeview/mutiCodeView/',mutiCodeView),
    path('codeview/getcode/', getcode),
    path('codeview/getAllStudent/', getAllStudent),
    path('codeview/getProblemList/', getProblemList),

]

handler400 = bad_request
handler403 = bad_request
handler404 = bad_request
handler500 = server_error
