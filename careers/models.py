from django.db import models
from django.contrib.auth.models import User
from Home.models import RecruiterData, StudentProfile

class Joblist(models.Model):
    options = (("Software","Software"),("IT","IT"),("Technical","Technical"),("Accounts","Accounts"),("Mamagement","Management"),("HR","HR"),("Marketing","Marketing"),("Other","Other"))
    Job_title = models.CharField(max_length = 255)
    job_category = models.CharField(max_length = 255,choices = options,null = True,blank = True)
    job_description = models.CharField(max_length = 255)
    Salary_start = models.IntegerField()
    Salary_end = models.IntegerField()
    Location = models.CharField(max_length = 255)
    mode_of_work = models.CharField(max_length = 255 , choices = (("Full time","Full time"),("Part Time","Part Time"),("Trainee","Trainee")))
    approval_status = models.BooleanField(default = False)
    recruiter = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank = True)
    company_profile = models.ForeignKey(RecruiterData, on_delete = models.CASCADE, null=True, blank = True)

    def __str__(self):
        return self.Job_title
    
class Jobapplication(models.Model):
    job = models.ForeignKey(Joblist,on_delete = models.CASCADE)
    applicant = models.ForeignKey(User,on_delete = models.CASCADE)
    applicant_profile = models.ForeignKey(StudentProfile,on_delete = models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add = True)
    status = models.BooleanField(null= True, blank = True)

class InterViewSchedule(models.Model):
    date = models.DateField(auto_now_add = False)
    time = models.TimeField(auto_now_add = False)
    applicant = models.ForeignKey(User,on_delete = models.CASCADE )
    job = models.ForeignKey(Joblist,on_delete = models.CASCADE)
    company =  models.ForeignKey(RecruiterData,on_delete = models.CASCADE)

