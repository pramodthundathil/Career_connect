from django.urls import path 
from .import views 

urlpatterns = [
    path("JobListing",views.JobListing,name="JobListing")
]