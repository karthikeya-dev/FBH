from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="home"),
    path("2",views.createaccount,name="createpage"),
    path("3",views.pingenerate,name="pingenerate"),
    path("4",views.otpvalidation,name="otpvalidation"),
    path("5",views.balence,name="bal"),
    path("6",views.withdrawal,name="withdraw"), 
    path("7",views.deposit,name="deposit"),
    path("8",views.transfer,name="transfer"),
]