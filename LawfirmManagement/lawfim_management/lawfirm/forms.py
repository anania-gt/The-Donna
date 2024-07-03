from django import forms
from django.contrib.auth.models import User
from . import models



#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#for Lawyer related form
class LawyerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class LawyerForm(forms.ModelForm):
    class Meta:
        model=models.Lawyer
        fields=['address','mobile','department','status','profile_pic']



# #for client related form
# class ClientUserForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','username','password']
#         widgets = {
#         'password': forms.PasswordInput()
#         }
# class ClientForm(forms.ModelForm):
#     #this is the extrafield for linking client and their assigend lawyer
#     assignedLawyerId=forms.ModelChoiceField(queryset=models.Lawyer.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
#     class Meta:
#         model=models.Client
#         fields=['address','mobile','status','case_complaint','profile_pic']


class ClientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class ClientForm(forms.ModelForm):
    
    assignedLawyerId=forms.ModelChoiceField(queryset=models.Lawyer.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Client
        fields=['address','mobile','status','case_complaint','profile_pic']


class AppointmentForm(forms.ModelForm):
    lawyerId=forms.ModelChoiceField(queryset=models.Lawyer.objects.all().filter(status=True),empty_label="Lawyer Name and Department", to_field_name="user_id")
    clientId=forms.ModelChoiceField(queryset=models.Client.objects.all().filter(status=True),empty_label="Client Name and case_complaint", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class ClientAppointmentForm(forms.ModelForm):
    lawyerId=forms.ModelChoiceField(queryset=models.Lawyer.objects.all().filter(status=True),empty_label="Lawyer Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

