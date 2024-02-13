from django.shortcuts import render, redirect 
from django.contrib import messages
from .froms import JobAddForm 
from .models import Joblist
from Home.models import RecruiterData

def JobListing(request):
    form = JobAddForm()
    jobs = Joblist.objects.filter(recruiter = request.user)
    if request.method == "POST":
        form = JobAddForm(request.POST)
        if form.is_valid():
            job = form.save()
            job.recruiter = request.user
            job.company_profile = RecruiterData.objects.get(user = request.user)
            job.save()
            messages.info(request,"Job Was Listed please wait for admin Approval..")

    context = {
        "form":form,
        "jobs":jobs
    }
    return render(request,"joblisting.html",context)
