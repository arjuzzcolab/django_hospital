from django.db import models
from accounts.models import patientProfile,loginTable


class Patient(models.Model):
    user = models.ForeignKey(patientProfile,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],default='Male')
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    occupation = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=20, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')],default='Single')

    def __str__(self):
        return f'{self.name}'

class Doctor(models.Model):
    logintable = models.ForeignKey(loginTable,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'Dr. {self.name} - {self.specialization}'


class Appointment(models.Model):
    
    patient_profile = models.ForeignKey(patientProfile, on_delete=models.CASCADE,null=True)
    patient_Name = models.CharField(max_length=200) 
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=200,null=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(unique=True,null=True)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
   
    def __str__(self):
        return  f'{self.patient_Name}'  

class MedicalHistory(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    medications = models.TextField()
    allergies = models.TextField()
    treatment_plan = models.TextField()

    def __str__(self):
        return f'Medical History of {self.patient}'


class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True)
    prescribed_date = models.DateTimeField(auto_now_add=True)
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    pharmacy = models.CharField(max_length=255)

    def __str__(self):
        return f'Prescription for {self.patient} by Dr. {self.doctor}'
    



    
class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()

class Department(models.Model):
    name = models.CharField(max_length=200)

class Resources(models.Model):
    name = models.CharField(max_length=200)


