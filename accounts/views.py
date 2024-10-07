from django.shortcuts import render,redirect
from accounts.models import patientProfile,loginTable
from django.contrib import messages
from django.contrib.auth import logout
# Create your views here.
def Registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
       

        if password and cpassword:
            if password == cpassword:
                if patientProfile.objects.filter(username=username).exists():
                    messages.info(request, 'Username already exists')
                    return redirect('register')
                
                elif loginTable.objects.filter(username=username).exists():
                    messages.info(request, 'Username already exists')
                    return redirect('register')
                else:
                    patientprofile = patientProfile(username=username,password=password,cpassword=cpassword)
 
                    logintable = loginTable(username=username,password=password,cpassword=cpassword,type='user')
                    patientprofile.save()
                   
                    logintable.save()
                    return redirect('login')
            else:
                messages.info(request, 'Password mismatch')
        else:
            messages.info(request, 'All fields are required')
        return redirect('register')
    return render(request, 'authentication/register.html')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            if loginTable.objects.filter(username=username,password=password).exists():
                user_details = loginTable.objects.get(username=username,password=password)
                user_name = user_details.username
                user_type = user_details.type
                if user_type == 'user':
                    request.session['username'] = user_name
                    return redirect('userview')
                elif user_type == 'doctor':
                    request.session['username'] = user_name
                    return redirect('doctorview')
                elif user_type == 'admin':
                    request.session['username'] = user_name
                    return redirect('admin')
            else:
                messages.error(request,'error')
        except:
            pass
    return render(request,'authentication/login.html')



def logOut(request):
    logout(request)
    return redirect('login')
