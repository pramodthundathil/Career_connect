from django.urls import path 
from .import views  

urlpatterns = [

    path("",views.Home,name="Home"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("SignIn",views.SignIn,name="SignIn"),
    path("RecruiterSignUp",views.RecruiterSignUp,name="RecruiterSignUp"),
    path("Index",views.Index,name="Index"),
    path("AdminIndex",views.AdminIndex,name="AdminIndex"),
    path("RecruiterIndex",views.RecruiterIndex,name="RecruiterIndex"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("ApproveRecruiter/<int:pk>",views.ApproveRecruiter,name="ApproveRecruiter"),
    path("StudentsProfile",views.StudentsProfile,name="StudentsProfile"),
    path("CreateStudentProfile",views.CreateStudentProfile,name="CreateStudentProfile"),
    path("AddNewEducation",views.AddNewEducation,name="AddNewEducation"),
    path("DeleteStudentEducation/<int:pk>",views.DeleteStudentEducation,name="DeleteStudentEducation"),
    path("updateprofiledata/<int:pk>",views.updateprofiledata,name="updateprofiledata"),
    path("UpdateResume/<int:pk>",views.UpdateResume,name="UpdateResume"),
    path("ChangeProfilephoto/<int:pk>",views.ChangeProfilephoto,name="ChangeProfilephoto"),
    path("AddResumewritingTip",views.AddResumewritingTip,name="AddResumewritingTip"),
    path("deletetip/<int:pk>",views.deletetip,name="deletetip"),
    path("ResumeTips",views.ResumeTips,name="ResumeTips"),
    
]  