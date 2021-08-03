"""osnov_sred URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('', views.data),
    path('upload/', views.upload, name='upload'),
    path('upload_amort_history/', views.upload_amort_history, name='upload_amort_history'),
    path('upload_change_bal_price/', views.upload_change_bal_price, name='upload_change_bal_price'),
    path('delete_data_main_t/', views.delete_data_main_t, name='delete_data_main_t'),
    path('delete_data_amort_t/', views.delete_data_amort_t, name='delete_data_amort_t'),
    path('upload_spisan/', views.upload_spisan, name='upload_spisan'),
    path('upload_employees/', views.upload_employees, name='upload_employees'),
]
