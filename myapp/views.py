from django.shortcuts import render, redirect,get_object_or_404
from .forms import BookForm,DoctorForm,AppointmentForm,MedicalHistoryForm,PrescriptionForm,LocationForm,ResourcesForm,DepartmentForm
from .models import Patient,Appointment,Doctor,MedicalHistory,Prescription,Location,Resources,Department 
from accounts.models import loginTable,patientProfile
from django.core.paginator import Paginator,EmptyPage
from accounts.forms import userForm
import stripe
from django.conf import settings
import datetime


def create(request):
    username = request.session.get('username')
    try:
        login_user = patientProfile.objects.get(username=username)
    except patientProfile.DoesNotExist:
        return redirect('login')
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
           
            patient = form.save(commit=False)
            patient.user = login_user
            patient.save()
            
          
            request.session['patient_email'] = patient.email
            
            return redirect('userview')
    else:
        form = BookForm()
    
    return render(request, 'user/create.html', {
        'form': form,
    })


def userview(request):
    username = request.session.get('username')  

    try:
      
        login_user = patientProfile.objects.get(username=username)
        
      
        patient = Patient.objects.get(user=login_user)
        
    except patientProfile.DoesNotExist:
        patient = None 
    except Patient.DoesNotExist:
        patient = None  

    
    return render(request, 'user/userview.html', {'patient': patient})




def create_doctor(request):
    username = request.session.get('username')
    try:
        login_doctor = loginTable.objects.get(username=username)
       
    except loginTable.DoesNotExist:
        return redirect('login')
    

    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.logintable = login_doctor
            doctor.save()
            
            return redirect('doctorview')
    else:
        form = DoctorForm()
    
    return render(request, 'doctor/create.html', {
        'form': form,
    })

def doctorview(request):
    username = request.session.get('username')
    try:
        login_doctor = loginTable.objects.get(username=username)
        doctor = Doctor.objects.filter(logintable=login_doctor) 
        context = {
            'has_doctor': doctor.exists(),
            'doctor': doctor.first() if doctor.exists() else None
        }
        
    except loginTable.DoesNotExist:
        context = {
            'has_doctor': False,
            'doctor': None
        }

    return render(request,'doctor/index.html',context)

def appointment(request):
    
    username = request.session.get('username')


    try:
        login_user = patientProfile.objects.get(username=username)
    except patientProfile.DoesNotExist:
        return redirect('login') 

    if request.method == 'POST':
 
        form = AppointmentForm(request.POST)
        if form.is_valid():
         
            appointment_data = form.cleaned_data

            appointment_data['fee'] = float(appointment_data['fee'])

            request.session['appointment_data'] = {
                'email': appointment_data['email'],
                'patient_Name': appointment_data['patient_Name'],  
                'contact_number': appointment_data['contact_number'],  
                'doctor_id': appointment_data['doctor'].id, 
                'doctor_name': appointment_data['doctor'].name,  
                'appointment_date': appointment_data['appointment_date'].isoformat(),  
                'fee': appointment_data['fee'],  
                'reason': appointment_data['reason']  
            }
            
            return redirect('payment_session')
    else:
      
        form = AppointmentForm()

  
    return render(request, 'user/appointment.html', {
        'form': form,
    })


stripe.api_key = settings.STRIPE_SECRET_KEY
def payment_session(request):
    appointment_data = request.session.get('appointment_data')
    if not appointment_data:
        return redirect('appointment')
    
    session = stripe.checkout.Session.create(
        payment_method_types= ['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': f"Appointment with {appointment_data['doctor_name']}",
                    },
                    'unit_amount': int(appointment_data['fee']*100),
                },
                'quantity':1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri('/profile/success/'),
        cancel_url= request.build_absolute_uri('/profile/cancel/')
    )
    return redirect(session.url,code=303)


def payment_success(request):
    appointment_data = request.session.get('appointment_data') 
    username = request.session.get('username') 

    if appointment_data:
        try:
        
            login_user = patientProfile.objects.get(username=username)
            doctor = Doctor.objects.get(id=appointment_data['doctor_id'])
            
      
            appointment = Appointment(
                patient_profile=login_user,
                doctor=doctor,  
                patient_Name = appointment_data['patient_Name'],
                email = appointment_data['email'],
                appointment_date=appointment_data['appointment_date'], 
                reason=appointment_data['reason'],  
                contact_number=appointment_data['contact_number'],  
                fee=appointment_data['fee'],  
            )
            appointment.save()  

         
            del request.session['appointment_data']

            
            return render(request, 'user/success.html', {'appointment': appointment})
        
        except patientProfile.DoesNotExist:
            return redirect('login')  

    return redirect('userview')  



def payment_cancel(request):
    return render(request,'user/cancel.html')







def appointments_option(request):
    username = request.session.get('username')
   

    try:
        login_user = patientProfile.objects.get(username=username)
       
        
        patient_appointments = Appointment.objects.filter(patient_profile=login_user)
        
        
   
        context = {
            'has_appointments': patient_appointments.exists(),
            'appointment': patient_appointments.first() if patient_appointments.exists() else None
        }
        
    except patientProfile.DoesNotExist:
        context = {
            'has_appointments': False,
            'appointment': None
        }

    return render(request, 'user/appointments_option.html', context)



def update_appointment(request,id):
    appointment = Appointment.objects.get(id=id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST,instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('userview')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request,'user/update.html',{'form':form,'appointment':appointment})

def delete(request,id):
    appointment = Appointment.objects.get(id=id)
    if request.method == 'POST':
        appointment.delete()
        return redirect('userview')
    return render(request,'user/delete.html',{'appointment':appointment})


def appointment_details(request):
    username = request.session.get('username')
    try:
        login_doctor = loginTable.objects.get(username=username)
        doctor = Doctor.objects.get(logintable=login_doctor)
        appointment = Appointment.objects.filter(doctor=doctor)

        paginator = Paginator(appointment,5)
        page_number = request.GET.get('page')
        try:
            page = paginator.get_page(page_number)
        except EmptyPage:
            page = paginator.page(page_number.num_pages)
    except (Appointment.DoesNotExist,Doctor.DoesNotExist):
        appointment = None
        doctor = None
        page = None


   
    return render(request,'doctor/list.html',{'appointment':appointment,'page':page,'doctor':doctor})

def detail(request,id):
    appointment = Appointment.objects.get(id=id)
    return render(request,'doctor/detail.html',{'appointment':appointment})



def details(request):
    username = request.session.get('username')
    try:
        login_doctor = loginTable.objects.get(username=username)
        doctor = Doctor.objects.get(logintable=login_doctor)
        appointment = Appointment.objects.filter(doctor=doctor)

        paginator = Paginator(appointment,5)
        page_number = request.GET.get('page')
        try:
            page = paginator.get_page(page_number)
        except EmptyPage:
            page = paginator.page(page_number.num_pages)
    except (Appointment.DoesNotExist,Doctor.DoesNotExist):
        appointment = None
        doctor=None
        page = None

   
    return render(request,'doctor/details.html',{'appointment':appointment,'page':page,'doctor':doctor})


def medical_create(request, appointment_id):  
    username = request.session.get('username')
   

    try:
        login_doctor = loginTable.objects.get(username=username)
        doctor = Doctor.objects.get(logintable=login_doctor)
      
        appointment = Appointment.objects.get(id=appointment_id)
        patient = Patient.objects.get(user=appointment.patient_profile)  

    except (Appointment.DoesNotExist, Patient.DoesNotExist):
        return redirect('doctorview')

    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            medical_history = form.save(commit=False)
            medical_history.patient = patient
            medical_history.doctor=doctor
            medical_history.save()
            return redirect('details')  
    else:
        form = MedicalHistoryForm()

    return render(request, 'doctor/medical.html', {'form': form, 'patient': patient,'appointment':appointment})


def medical_details(request):
    username= request.session.get('username')
    try:
        patient_profile = patientProfile.objects.get(username=username)
        patient = Patient.objects.get(user=patient_profile)
        
    except Patient.DoesNotExist:
        patient=None
        
    
    medical = MedicalHistory.objects.filter(patient=patient)
    
    return render(request,'user/medical_details.html',{'medical':medical,'patient':patient})

def update_medical_show(request,id):
    username = request.session.get('username')
    try:
        appointment = Appointment.objects.get(id=id)
        patient = Patient.objects.get(user=appointment.patient_profile)
        login_doctor = loginTable.objects.get(username=username)
        doctor = Doctor.objects.get(logintable=login_doctor)
    except (loginTable.DoesNotExist,Patient.DoesNotExist,Doctor.DoesNotExist):
        return redirect('login')
    medical_show = MedicalHistory.objects.filter(patient=patient,doctor=doctor)
    return render(request,'doctor/update_medical_show.html',{'medical_show':medical_show})


def medical_update(request,id):
    medical = MedicalHistory.objects.get(id=id)
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST,instance=medical)
        if form.is_valid():
            form.save()
            return redirect('doctorview')
    else:
        form = MedicalHistoryForm(instance=medical)
    return render(request,'doctor/medical_update.html',{'form':form,'medical':medical})

def medical_delete(request,id):
    medical = MedicalHistory.objects.get(id=id)
    if request.method == 'POST':
        medical.delete()
        return redirect('doctorview')
    return render(request,'doctor/medical_delete.html',{'medical':medical})

def prescription(request):
    username = request.session.get('username')
    try:
        login_doctor = loginTable.objects.get(username=username)
        doctor = Doctor.objects.get(logintable=login_doctor)
        appointment =Appointment.objects.get(doctor=doctor)
    except Appointment.DoesNotExist:
        appointment=None
    except Doctor.DoesNotExist:
        doctor=None
        appointment=None
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = doctor
            prescription.save()
            return redirect('doctorview')
    else:
        form = PrescriptionForm()
    return render(request,'doctor/prescription.html',{'form':form,'appointment':appointment,'doctor':doctor})

def prescription_list(request):
    username = request.session.get('username')
    try:
        login_user = patientProfile.objects.get(username=username)
        
      
        appointments = Appointment.objects.filter(patient_profile=login_user)
    except patientProfile.DoesNotExist:
        appointments = []  

    
    prescriptions = Prescription.objects.filter(appointment__in=appointments)
    
    return render(request, 'user/presc_list.html', {'prescription': prescriptions})


def healthview(request):
    return render(request,'user/health.html')

def healthtips(request):
    return render(request,'user/tips.html')

def prevention(request):
    return render(request,'user/prevention.html')

def resource(request):
    return render(request,'user/resource.html')




def adminview(request):
    return render(request,'admin/adminview.html')

def user_list(request):
    user = patientProfile.objects.all()
    paginator = Paginator(user,2)
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(page_number.num_pages)
    return render(request,'admin/list.html',{'user':user,'page':page})

def user_update(request,id):
    user = patientProfile.objects.get(id=id)
    if request.method == 'POST':
        form = userForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = userForm(instance=user)
    return render(request,'admin/update.html',{'form':form})


def user_delete(request,id):
    user = patientProfile.objects.get(id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request,'admin/delete.html',{'user':user})


def manage_facility(request):
    return render(request,'admin/facility.html')

def location_create(request):
    location = Location.objects.all()
    paginator = Paginator(location,3)
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(page_number.num_pages)
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_create')
    else:
        form = LocationForm()
    return render(request,'admin/location_create.html',{'form':form,'location':location,'page':page})

def location_update(request,id):
    location = Location.objects.get(id=id)
    if request.method == 'POST':
        form = LocationForm(request.POST,instance=location)
        if form.is_valid():
            form.save()
            return redirect('location_create')
    else:
        form = LocationForm(instance=location)
    return render(request,'admin/location_update.html',{'form':form})

def location_delete(request,id):
    location = Location.objects.get(id=id)
    if request.method == 'POST':
        location.delete()
        return redirect('location_create')
    return render(request,'admin/location_delete.html',{'location':location})


def dept_create(request):
    dept = Department.objects.all()
    paginator = Paginator(dept,3)
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(page_number.num_pages)
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dept_create')
    else:
        form = DepartmentForm()
    return render(request,'admin/department_create.html',{'form':form,'dept':dept,'page':page})

def dept_update(request,id):
    dept = Department.objects.get(id=id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST,instance=dept)
        if form.is_valid():
            form.save()
            return redirect('dept_create')
    else:
        form = DepartmentForm(instance=dept)
    return render(request,'admin/dept_update.html',{'form':form})

def dept_delete(request,id):
    dept = Department.objects.get(id=id)
    if request.method == 'POST':
        dept.delete()
        return redirect('dept_create')
    return render(request,'admin/dept_delete.html',{'dept':dept})



def res_create(request):
    res = Resources.objects.all()
    paginator = Paginator(res,3)
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(page_number.num_pages)
    if request.method == 'POST':
        form = ResourcesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('res_create')
    else:
        form = ResourcesForm()
    return render(request,'admin/res_create.html',{'form':form,'res':res,'page':page})

def res_update(request,id):
    res = Resources.objects.get(id=id)
    if request.method == 'POST':
        form = ResourcesForm(request.POST,instance=res)
        if form.is_valid():
            form.save()
            return redirect('res_create')
    else:
        form = ResourcesForm(instance=res)
    return render(request,'admin/res_update.html',{'form':form})

def res_delete(request,id):
    res = Resources.objects.get(id=id)
    if request.method == 'POST':
        res.delete()
        return redirect('res_create')
    return render(request,'admin/res_delete.html',{'res':res})


def appointment_show(request):
    appointment = Appointment.objects.all()
    return render(request,'admin/appointment_show.html',{'appointment':appointment})

def appo_update(request,id):
    appointment = Appointment.objects.get(id=id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST,instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_show')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request,'admin/appo_update.html',{'form':form})

def appo_delete(request,id):
    appo = Appointment.objects.get(id=id)
    if request.method == 'POST':
        appo.delete()
        return redirect('appointment_show')
    return render(request,'admin/appo_delete.html',{'appo':appo})