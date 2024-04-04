from django.shortcuts import render, redirect 
from django.contrib import messages
from .froms import JobAddForm 
from .models import Joblist, Jobapplication, InterViewSchedule
from Home.models import RecruiterData, StudentProfile, Education


import PyPDF2
import PyPDF2
import re
import string
import pandas as pd
import matplotlib.pyplot as plt
import imageio

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

def DeleteJob(request,pk):
    Joblist.objects.get(id = pk).delete()
    messages.success(request,"Job Deleted Success.....")
    return redirect("JobListing")

def ApproveJob(request,pk):
    job = Joblist.objects.get(id = pk)
    job.approval_status = True
    job.save()
    return redirect("AdminIndex")

def JobViewUser(request,pk):
    job = Joblist.objects.get(id = pk)

    context = {
        "job":job
    }
    return render(request,"jobview.html",context)

def JobViewRecruiter(request,pk):
    job = Joblist.objects.get(id = pk)
    applicants = Jobapplication.objects.filter(job = job)
    
    context = {
        "job":job,
        "students":applicants
    }
    return render(request,"jobsingleviewrecruter.html",context)

def Applaytojob(request,pk):

    job = Joblist.objects.get(id = pk)

    if Jobapplication.objects.filter(applicant = request.user, job = job).exists():
        messages.info(request,"You are alredy applied to this job")
        return redirect("JobViewUser", pk = pk )
    else:
        application = Jobapplication.objects.create(applicant = request.user, job = job,applicant_profile = StudentProfile.objects.get(user = request.user ) )
        application.save()
        messages.success(request,"Application Submited Success.....")
        return redirect("JobViewUser", pk= pk)
    return redirect("JobViewUser", pk= pk)

def deleteapplication(request,pk):
    Jobapplication.objects.get(id = pk).delete()
    messages.info(request,"Application delete Success.....")

    return redirect("AdminIndex")

def studentProfileRecruiterView(request,pk):
    applicant = Jobapplication.objects.get(id = pk)
    applicatedu = Education.objects.filter(user = applicant.applicant)
    context = {
        "applicant":applicant,
        "applicatedu":applicatedu
    }
    return render(request,"studentprofilerecruterview.html",context)

def InterviewSchedule(request,pk):
    job = Jobapplication.objects.get(id = pk)
    if request.method == "POST":
        date = request.POST["date"]
        time = request.POST["time"]
        interview = InterViewSchedule.objects.create(date = date,time = time,applicant = job.applicant, job = job.job, company = job.job.company_profile)
        interview.save()
        messages.info(request,"Interview Scheduled.....")
        return redirect("studentProfileRecruiterView", pk = pk)


    return redirect("studentProfileRecruiterView", pk = pk)

def interviewSchedules(request):
    company = RecruiterData.objects.get(user = request.user)
    interview = InterViewSchedule.objects.filter(company = company)
    context = {
        "interview":interview
    }
    return render(request,"interviewschedules.html",context)

def interviewSchedulesUser(request):
    
    interview = InterViewSchedule.objects.filter(applicant = request.user)
    context = {
        "interview":interview
    }
    return render(request,"interviewschedulesuser.html",context)


def Deleteinterview(request,pk):
    InterViewSchedule.objects.get(id = pk).delete()
    messages.info(request,"Interview Deleted.....")
    return redirect("interviewSchedules")
