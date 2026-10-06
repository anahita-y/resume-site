from django.urls import path 
from . import views

app_name = "resumes"

urlpatterns = [
    path("" , views.resume_create , name = "create") ,
    path("success/<uuid:token>/" , views.success , name = "success") , 
    path("download/<uuid:token>/" , views.download , name = "download") ,
    path("preview/<int:pk>/" , views.resume_preview ,  name = "preview") ,
]
