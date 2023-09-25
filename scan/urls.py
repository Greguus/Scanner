from django.urls import path
from . import views

urlpatterns = [
    path ("", views.index, name="index"),
    path ("ip_check", views.ip_check, name="ip_check"),
    path ("subnet", views.subnet_scan, name="subnet_scan"),
    path ("subnet_test", views.subnet_scan, name="subnet_test"),
]
