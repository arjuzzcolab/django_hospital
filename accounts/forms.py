from .models import patientProfile
from django import forms
class userForm(forms.ModelForm):
    class Meta:
        model = patientProfile
        fields = [ 'username', 'password']
        widgets = {
            
            
        
            'username': forms.TextInput(attrs={'class': 'form-control'}),

            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }
