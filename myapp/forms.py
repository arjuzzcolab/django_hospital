from django import forms
from .models import Patient,Doctor,Appointment,MedicalHistory,Prescription,Location,Resources,Department

class BookForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [ 'name','date_of_birth','gender', 'contact_number','email','address','occupation','marital_status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter address'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter occupation'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'contact_number', 'email']


        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Doctor Name'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Specialization'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
        }

        labels = {
            'name': 'Doctor Name',
            'specialization': 'Specialization',
            'contact_number': 'Contact Number',
            'email': 'Email Address',
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['email','fee','patient_Name','doctor','appointment_date', 'reason','contact_number']

      
        widgets = {
            'patient_Name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            
            'appointment_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Reason for Appointment'}),
            
        }
    fee = forms.DecimalField(
        initial=1000, 
        max_digits=10, 
        decimal_places=2, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )




class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['diagnosis', 'medications', 'allergies', 'treatment_plan']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter diagnosis'}),
            'medications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter medications'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter allergies'}),
            'treatment_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter treatment plan'}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['appointment', 'medication_name', 'dosage', 'instructions', 'pharmacy']
        widgets = {
            
            'appointment': forms.Select(attrs={'class': 'form-control'}),
            'medication_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter medication name'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter dosage'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter instructions'}),
            'pharmacy': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter pharmacy'}),
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Location Name',
                'style': 'width: 300px;',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Location Address',
                'rows': 4,
                
                'style': 'width: 300px;',
            }),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Department Name',
                'style': 'width: 300px;',
            }),
        }

class ResourcesForm(forms.ModelForm):
    class Meta:
        model = Resources
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Resource Name',
                'style': 'width: 300px;',
            }),
        }