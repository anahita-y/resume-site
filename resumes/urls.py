from django.urls import path 
from . import views

app_name = "resumes"

urlpatterns = [
    path("" , views.resume_create , name = "create") ,
    path("success/" , views.success , name = "success") , 
]
