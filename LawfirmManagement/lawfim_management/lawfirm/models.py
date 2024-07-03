from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import User



departments=[('Bankruptcy Lawyer','Bankruptcy Lawyer'),
('Business Lawyer (Corporate Lawyer)','Business Lawyer (Corporate Lawyer)'),
('Constitutional Lawyer','Constitutional Lawyer'),
('Criminal Defense Lawyer','Criminal Defense Lawyer'),
('Employment and Labor Lawyer','Employment and Labor Lawyer'),
('Entertainment Lawyer','Entertainment Lawyer'),
('Estate Planning Lawyer','Estate Planning Lawyer'),
('Family Lawyer','Family Lawyer'),
('Immigration Lawyer','Immigration Lawyer'),
('Intellectual Property (IP) Lawyer','Intellectual Property (IP) Lawyer'),
('Personal Injury Lawyer','Personal Injury Lawyer'),
('Tax Lawyer','Tax Lawyer')
]

class Lawyer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/LawyerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Criminal Defense Lawyer')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Client(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/ClientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    case_complaint = models.CharField(max_length=100,null=False)
    assignedLawyerId = models.PositiveIntegerField(null=True)
    complaintDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.case_complaint+")"


class Appointment(models.Model):
    clientId=models.PositiveIntegerField(null=True)
    lawyerId=models.PositiveIntegerField(null=True)
    clientName=models.CharField(max_length=40,null=True)
    lawyerName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)



class ClientDischargeDetails(models.Model):
    clientId=models.PositiveIntegerField(null=True)
    clientName=models.CharField(max_length=40)
    assignedlawyerName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    case_complaints = models.CharField(max_length=100,null=True)

    complaintDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    hoursCharge=models.PositiveIntegerField(null=False)
    resourceCost=models.PositiveIntegerField(null=False)
    lawyerFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)


