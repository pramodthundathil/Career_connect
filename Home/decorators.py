from django.http import HttpResponse
from django.shortcuts import redirect
from .models import RecruiterData, Personality


#decorator for user redirect...............
def unautenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('Index')
        else:
            return view_func(request,*args,**kwargs)
        
    return wrapper_func

# allowed user decorators................
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

#decorators for user wise redirect pages...............
def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == None:
            return view_func(request, *args, **kwargs)
            
        if group == 'student':
            return view_func(request, *args, **kwargs)
        
        if group == 'recruiter':
            return redirect('RecruiterIndex')
        
        if group == 'admin':
            return redirect('AdminIndex')
              
    return wrapper_function


def UnapprovedRecruiter(func):
    def warpper_fun(request,*args,**kwargs):
        try:
            recruiter = RecruiterData.objects.get(user = request.user)
        except:
            return HttpResponse("Not allowed")
        if recruiter.approval_status == True:
            return  func(request,*args,**kwargs)
        else:
            text = ''''
            <h1 style='color:blue;text-align:center'>
            Your Request is not Yet Approved Please wait for approval 
            <a href="SignOut" style='padding:10px 20px;border-radius:10px;background-color:red;color:white'>Logout</a>
            </h1>
            '''
            return HttpResponse(text)
        
    return warpper_fun

def ApptitudetestDone(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.groups.all()[0].name == "student":
            if Personality.objects.filter(user = request.user).exists():
                return view_func(request,*args,**kwargs)
            else:
                return redirect("Aptitudetest")
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func
