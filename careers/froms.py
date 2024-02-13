from django.forms import ModelForm 

from .models import Joblist

class JobAddForm(ModelForm):
    class Meta:
        model = Joblist 
        fields = ["Job_title","job_description","job_category","mode_of_work","Salary_start","Salary_end","Location" ]