from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("vm_form/", views.vm_form, name="vm_form"),
]