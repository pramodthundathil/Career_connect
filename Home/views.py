from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserAddForm
from django.contrib.auth.models import User, Group
from .models import RecruiterData, Education, Experiance, StudentProfile, ResumeWritingTips
from .decorators import admin_only, UnapprovedRecruiter
from careers.models import Joblist, Jobapplication, InterViewSchedule


def Home(request):
    recruiter = RecruiterData.objects.filter(approval_status = True)
    jobs = Joblist.objects.filter(approval_status = True)
    context = {
        "companies":recruiter,
        "jobs":jobs
    }
    return render(request,'index.html',context)

@admin_only
def Index(request):
    recruiter = RecruiterData.objects.filter(approval_status = True)
    job = Joblist.objects.filter(approval_status = True)
    interview = InterViewSchedule.objects.filter(applicant = request.user)
    context = {
        "companies":recruiter,
        "jobs":job,
        "interview":interview
    }
    return render(request,'homeindex.html',context)

def AdminIndex(request):
    approved_recruitrs = RecruiterData.objects.filter(approval_status = True)
    unapproved_recruitrs = RecruiterData.objects.filter(approval_status = False)
    job = Joblist.objects.filter(approval_status = True)
    apjob = Joblist.objects.filter(approval_status = False)
    jobapplication = Jobapplication.objects.all()
    tip = ResumeWritingTips.objects.all()


    context = {
        "approved_recruitrs":approved_recruitrs,
        "unapproved_recruitrs":unapproved_recruitrs,
        "approved_recruitrs_count": len(approved_recruitrs),
        "unapproved_recruitrs_count": len(unapproved_recruitrs),
        "job":job,
        "job_count":len(job),
        "apjob":apjob,
        "apjob_count":len(apjob),
        "jobapplication":jobapplication,
        "jobapplication_count":len(jobapplication),
        "tip":tip
    }
    return render(request,'adminindex.html',context)

@UnapprovedRecruiter
def RecruiterIndex(request):
    return render(request,'recruiterindex.html')

def SignIn(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user1 = authenticate(request, username = username , password = password)
        
        if user1 is not None:
            
            request.session['username'] = username
            request.session['password'] = password
            login(request, user1)
            return redirect('Index')
        
        else:
            messages.info(request,'Username or Password Incorrect')
            return redirect('SignIn')
    return render(request,"login.html")


def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        # fname = request.POST["fname"]
        # email = request.POST["email"]
        # uname = request.POST["uname"]
        # pswd = request.POST["pswd"]
        # pswd1 = request.POST["pswd1"]

        # if pswd != pswd1:
        #     messages.info(request,"Password Do not Matches..")
        #     return redirect("SignUp")
        # if User.objects.filter(username = uname).exists():
        #     messages.info(request,"Username alredy exists user another username")
        #     return redirect("SignUp")
        # if User.objects.filter(email = email).exists():
        #     messages.info(request,"Email alredy exists user another email")
        #     return redirect("SignUp")

        form = UserAddForm(request.POST)

        if form.is_valid:
            user = form.save()
            user.save()
            group = Group.objects.get(name='student')
            user.groups.add(group)
            messages.success(request,"User Created.. Please Login....")
            return redirect("SignIn")
        
    return render(request,"register.html",{"form":form})



def RecruiterSignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        dis = request.POST["dis"]
        fow = request.POST["fow"]
        logo = request.FILES["logo"]
        form = UserAddForm(request.POST)

        if form.is_valid:
            user = form.save()
            user.save()
            group = Group.objects.get(name='recruiter')
            user.groups.add(group)
            recruiter = RecruiterData.objects.create(user = user,profile = dis,conmpany_logo_or_photo = logo, field_of_work = fow)
            recruiter.save()
            messages.success(request,"Recruiter Created.. Please wait for approvel....")
            return redirect("SignIn")
        
    return render(request,"recruterregister.html",{"form":form})

def SignOut(request):
    logout(request)
    return redirect('SignIn')

def ApproveRecruiter(request,pk):
    recruiter = RecruiterData.objects.get(id = pk)
    recruiter.approval_status = True
    recruiter.save()
    messages.info(request,"Reruiter approved successfully......")
    return redirect("AdminIndex") 

def StudentsProfile(request):
    try:
        profile = StudentProfile.objects.get(user = request.user)
        edu = Education.objects.filter(user = request.user)
        # exp = Experiance.objects.get(user = request.user)
    except:
        return render(request,"profileupdate.html")
    
    context = {
        "profile":profile,
        "edu":edu
    }

    return render(request,"studentprofile.html",context)

def CreateStudentProfile(request):
    if request.method == "POST":
        lname = request.POST["lname"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        bio = request.POST["bio"]
        lng = request.POST["lng"]
        skills = request.POST["skills"] 
        photo = request.FILES["photo"]
        resume = request.FILES["resume"]
        institution = request.POST["institution"]
        year = request.POST["year"]
        stream = request.POST["stream"]
        cgpa = request.POST["cgpa"]

        profile = StudentProfile.objects.create(user = request.user, last_name = lname , Phone_number = phone , address = address ,Bio_Discription = bio , Languages = lng , resume = resume , Photo = photo, Skills = skills   )

        education = Education.objects.create(user = request.user,stream = stream,institution =institution,year = year,CGPA =cgpa  )

        profile.save()
        education.save()

        return redirect("StudentsProfile")
    
def AddNewEducation(request):
    if request.method == "POST":
        institution = request.POST["institution"]
        year = request.POST["year"]
        stream = request.POST["stream"]
        cgpa = request.POST["cgpa"]
        education = Education.objects.create(user = request.user,stream = stream,institution =institution,year = year,CGPA =cgpa )
        education.save()
        messages.info(request,"New Education added..")
        return redirect("StudentsProfile")

    return redirect("StudentsProfile")

def DeleteStudentEducation(request,pk):
    Education.objects.get(id = pk).delete()
    messages.info(request,"Education data deleted..")
    return redirect("StudentsProfile")

def updateprofiledata(request,pk):
    profile = StudentProfile.objects.get(id = pk)

    if request.method == "POST":
        dis = request.POST['dis']
        mob = request.POST['mob']
        email = request.POST['email']
        address = request.POST['address']

        profile.Bio_Discription = dis 
        profile.Phone_number = mob 
        profile.address = address
        profile.save()
        user = request.user
        user.email = email 
        user.save()
        messages.info(request,"Data Updated..")
        return redirect("StudentsProfile")
    return redirect("StudentsProfile")

def UpdateResume(request,pk):
    profile = StudentProfile.objects.get(id = pk)
    
    if request.method == "POST":
        res = request.FILES['resume']
        profile.resume.delete()
        profile.resume = res
        profile.save()
        messages.info(request,"Data Updated..")
        return redirect("StudentsProfile")
    return redirect("StudentsProfile")

def ChangeProfilephoto(request,pk):
    profile = StudentProfile.objects.get(id = pk)
    
    if request.method == "POST":
        res = request.FILES['photo']
        profile.Photo.delete()
        profile.Photo = res
        profile.save()
        messages.info(request,"Data Updated..")
        return redirect("StudentsProfile")
    return redirect("StudentsProfile")

def AddResumewritingTip(request):
    if request.method == "POST":

        tip = ResumeWritingTips.objects.create(tip_title = request.POST['title'], tip = request.POST['tip'])
        tip.save()
        messages.info(request,"Data Updated..")
        return redirect("AdminIndex")


    return redirect("AdminIndex")

def deletetip(request,pk):
    ResumeWritingTips.objects.get(id = pk).delete()
    messages.info(request,"Data deleted..")
    return redirect("AdminIndex")

def ResumeTips(request):
    tip = ResumeWritingTips.objects.all()
    return render(request,"tips.html",{"tip":tip})

def ComapnyView(request,pk):

    company = RecruiterData.objects.get(id = pk)
    context = {
        "company":company
    }
    return render(request,"viewcompany.html",context)

