from django.urls import path 
from .import views 

urlpatterns = [
    path("JobListing",views.JobListing,name="JobListing"),
    path("ApproveJob/<int:pk>",views.ApproveJob,name="ApproveJob"),
    path("JobViewUser/<int:pk>",views.JobViewUser,name="JobViewUser"),
    path("JobViewRecruiter/<int:pk>",views.JobViewRecruiter,name="JobViewRecruiter"),
    path("Applaytojob/<int:pk>",views.Applaytojob,name="Applaytojob"),
    path("DeleteJob/<int:pk>",views.DeleteJob,name="DeleteJob"),
    path("deleteapplication/<int:pk>",views.deleteapplication,name="deleteapplication"),
    path("studentProfileRecruiterView/<int:pk>",views.studentProfileRecruiterView,name="studentProfileRecruiterView"),
    path("InterviewSchedule/<int:pk>",views.InterviewSchedule,name="InterviewSchedule"),
    path("interviewSchedules",views.interviewSchedules,name="interviewSchedules"),
    path("interviewSchedulesUser",views.interviewSchedulesUser,name="interviewSchedulesUser"),
    path("Deleteinterview/<int:pk>",views.Deleteinterview,name="Deleteinterview"),
    
]