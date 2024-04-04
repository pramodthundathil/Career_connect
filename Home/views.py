from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserAddForm
from django.contrib.auth.models import User, Group
from .models import RecruiterData, Education, Experiance, StudentProfile, ResumeWritingTips, Personality
from .decorators import admin_only, UnapprovedRecruiter, ApptitudetestDone, unautenticated_user
from careers.models import Joblist, Jobapplication, InterViewSchedule
from django.contrib.auth.decorators import login_required

import matplotlib.pyplot as plt
import PyPDF2
import PyPDF2
import re
import string
import pandas as pd
import matplotlib.pyplot as plt
import imageio
import pandas as pd
import numpy as np
import csv

@unautenticated_user
def Home(request):
    recruiter = RecruiterData.objects.filter(approval_status = True)
    jobs = Joblist.objects.filter(approval_status = True)
    context = {
        "companies":recruiter,
        "jobs":jobs
    }
    return render(request,'index.html',context)

@admin_only
@ApptitudetestDone
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


@login_required(login_url='SignIn')
def Aptitudetest(request):
    
    if request.method =="POST":
        Gender = request.POST["Gender"]
        age = request.POST["age"]
        Openness = request.POST["Openness"]
        Neuroticism = request.POST["Neuroticism"]
        Agreeableness = request.POST["Agreeableness"]
        Conscientiousness = request.POST["Conscientiousness"]
        Extraversion = request.POST["Extraversion"]
        
        if Personality.objects.filter(user = request.user).exists():
            data = Personality.objects.get(user = request.user)
            data.Openness = Openness
            data.Neuroticiem = Neuroticism
            data.Agreeableness = Agreeableness
            data.Conscientiousness = Conscientiousness
            data.Extraversion = Extraversion
            data.Gender = Gender
            data.Age = age
            
            data.save()
            messages.info(request,"Aptitude test success")
            return redirect('Index')
            
        else:
        
            datas = Personality.objects.create(user = request.user,Gender = Gender,Age = age,Openness = Openness,Neuroticiem= Neuroticism,Agreeableness = Agreeableness,Conscientiousness = Conscientiousness, Extraversion = Extraversion)
            datas.save()
            data = pd.read_csv('Home/training_dataset.csv')
            array = data.values

            userdata = [Gender,int(age),int(Openness),int(Neuroticism),int(Conscientiousness),int(Agreeableness),int(Extraversion)]
            
            flag = 0
            for i in array:
                j = list(i)
                j.pop(-1)
                print(j,userdata)
                if userdata == j:
                    print("Data Finded")
                    flag = 1
                    val = i 
                    break
                
            if flag == 0:
                list1 = ["extraverted","serious","responsible","lively","dependable",]
                import random
                val2 = random.choice(list1)
                userdata.append(val2)
                with open('Home/training_dataset.csv', 'a') as f_object:
                    writer_object = csv.writer(f_object)
                    writer_object.writerow(userdata)
                    f_object.close()
                datas.Personality = val2
                datas.save()

            if flag == 1:
                
                datas.Personality = val[-1]
                datas.save()

            messages.info(request,"Aptitude test success")
            return redirect("Index")
        
    return render(request,'resumeupload.html')


@login_required(login_url='SignIn')
def PredictPersonality(request,pk):
    data = pd.read_csv('Home/training_dataset.csv')
    array = data.values
    dataarray = np.array(array)
    applicant = Jobapplication.objects.get(id = pk)

    dmodel = Personality.objects.get(user = applicant.applicant)
    userdata = [dmodel.Gender,int(dmodel.Age),int(dmodel.Openness),int(dmodel.Neuroticiem),int(dmodel.Conscientiousness),int(dmodel.Agreeableness),int(dmodel.Extraversion)]
    def recursive_func():
        flag = 0
        for i in array:
            j = list(i)
            j.pop(-1)
            print(j,userdata)
            if userdata == j:
                print("Data Finded")
                flag = 1
                val = i 
                break
            
        if flag == 0:
            list1 = ["extraverted","serious","responsible","lively","dependable",]
            import random
            val2 = random.choice(list1)
            userdata.append(val2)
            with open('Home/training_dataset.csv', 'a') as f_object:
                writer_object = csv.writer(f_object)
                writer_object.writerow(userdata)
                f_object.close()
            dmodel = Personality.objects.get(user = applicant.applicant)
            dmodel.Personality = val2
            dmodel.save()
            return redirect("PredictionResults",pk = applicant.applicant.id)
            
        if flag == 1:
            dmodel = Personality.objects.get(user = applicant.applicant)
            dmodel.Personality = val[-1]
            dmodel.save()
            return redirect("PredictionResults",pk = applicant.applicant.id)

    return recursive_func()


@login_required(login_url='SignIn')
def PredictionResults(request,pk):
    user = User.objects.get(id = pk)
    dmodel = Personality.objects.filter(user = user)
    dmodel1 = Personality.objects.get(user = user)
    student = StudentProfile.objects.get(user = user)
    resume = student.resume.url
    strvalue = str(resume)[1:]
    print(strvalue)
    pdfFileObj = open(strvalue,'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    num_pages = len(pdfReader.pages)

    count = 0
    text = ""

    while count < num_pages:
        pageObj = pdfReader.pages[count]
        count +=1
        text += pageObj.extract_text()
    
    
    text = text.lower()

    text = re.sub(r'\d+','',text)
    text = text.translate(str.maketrans('','',string.punctuation))

    print(text)

    terms = {'Quality/Six Sigma':['black belt','capability analysis','control charts','doe','dmaic','fishbone',
                              'gage r&r', 'green belt','ishikawa','iso','kaizen','kpi','lean','metrics',
                              'pdsa','performance improvement','process improvement','quality',
                              'quality circles','quality tools','root cause','six sigma',
                              'stability analysis','statistical analysis','tqm'],      
        'Operations management':['automation','bottleneck','constraints','cycle time','efficiency','fmea',
                                 'machinery','maintenance','manufacture','line balancing','oee','operations',
                                 'operations research','optimization','overall equipment effectiveness',
                                 'pfmea','process','process mapping','production','resources','safety',
                                 'stoppage','value stream mapping','utilization'],
        'Supply chain':['abc analysis','apics','customer','customs','delivery','distribution','eoq','epq',
                        'fleet','forecast','inventory','logistic','materials','outsourcing','procurement',
                        'reorder point','rout','safety stock','scheduling','shipping','stock','suppliers',
                        'third party logistics','transport','transportation','traffic','supply chain',
                        'vendor','warehouse','wip','work in progress'],
        'Project management':['administration','agile','budget','cost','direction','feasibility analysis',
                              'finance','kanban','leader','leadership','management','milestones','planning',
                              'pmi','pmp','problem','project','risk','schedule','scrum','stakeholders'],
        'Data analytics':['analytics','api','aws','big data','busines intelligence','clustering','code',
                          'coding','data','database','data mining','data science','deep learning','hadoop',
                          'hypothesis test','iot','internet','machine learning','modeling','nosql','nlp',
                          'predictive','programming','python','r','sql','tableau','text mining',
                          'visualuzation'],
        'Healthcare':['adverse events','care','clinic','cphq','ergonomics','healthcare',
                      'health care','health','hospital','human factors','medical','near misses',
                      'patient','reporting system']}

    quality = 0
    operations = 0
    supplychain = 0
    project = 0
    data = 0
    healthcare = 0

    scores = []

    for area in terms.keys():
        
        if area == 'Quality/Six Sigma':
            for word in terms[area]:
                if word in text:
                    quality +=1
            scores.append(quality)
        
        elif area == 'Operations management':
            for word in terms[area]:
                if word in text:
                    operations +=1
            scores.append(operations)
        
        elif area == 'Supply chain':
            for word in terms[area]:
                if word in text:
                    supplychain +=1
            scores.append(supplychain)
        
        elif area == 'Project management':
            for word in terms[area]:
                if word in text:
                    project +=1
            scores.append(project)
        
        elif area == 'Data analytics':
            for word in terms[area]:
                if word in text:
                    data +=1
            scores.append(data)
        
        else:
            for word in terms[area]:
                if word in text:
                    healthcare +=1
            scores.append(healthcare)
        
    summary = pd.DataFrame(scores,index=terms.keys(),columns=['score']).sort_values(by='score',ascending=False)
    print(summary)

    pie = plt.figure(figsize=(10,10))
    plt.pie(summary['score'], labels=summary.index, explode = (0.1,0,0,0,0,0), autopct='%1.0f%%',shadow=True,startangle=90)
    plt.title('Resume Decomposition by Areas')
    plt.axis('equal')
    pie.savefig('resume_screening_results.png')
    import os
    my_path = os.path.abspath(__file__) # Figures out the absolute path for you in case your working directory moves around.
    my_file = 'graph.png'
    
    pie.savefig(os.path.join('static/img/', my_file)) 
    
    userprofile = StudentProfile.objects.filter(user = request.user)
    
    context = {
        "dmodel":dmodel,
        "summary":summary,
        "score":scores,
        "userprofile":userprofile,
        
    }
    return render(request,'predictionresult.html',context)  

