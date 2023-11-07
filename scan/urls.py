from django.urls import path
from . import views

urlpatterns = [
    path ("", views.index, name="index"),
    path ("ip_check", views.ip_check, name="ip_check"),
    path ("subnet", views.subnet_scan, name="subnet_scan"),
    #path ("subnet_test", views.subnet_test, name="subnet_test"),
    path ("subnet_results", views.subnet_results, name="subnet_results"),
]
