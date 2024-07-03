from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'lawfirm/index.html')


#for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'lawfirm/adminclick.html')


#for showing signup/login button for lawyer
def lawyerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'lawfirm/lawyerclick.html')


#for showing signup/login button for client
def clientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'lawfirm/clientclick.html')





def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'lawfirm/adminsignup.html',{'form':form})




def lawyer_signup_view(request):
    userForm=forms.LawyerUserForm()
    lawyerForm=forms.LawyerForm()
    mydict={'userForm':userForm,'lawyerForm':lawyerForm}
    if request.method=='POST':
        userForm=forms.LawyerUserForm(request.POST)
        lawyerForm=forms.LawyerForm(request.POST,request.FILES)
        if userForm.is_valid() and lawyerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            lawyer=lawyerForm.save(commit=False)
            lawyer.user=user
            lawyer=lawyer.save()
            my_lawyer_group = Group.objects.get_or_create(name='LAWYER')
            my_lawyer_group[0].user_set.add(user)
        return HttpResponseRedirect('lawyerlogin')
    return render(request,'lawfirm/lawyersignup.html',context=mydict)


# def client_signup_view(request):
#     userForm=forms.ClientUserForm()
#     clientForm=forms.ClientForm()
#     mydict={'userForm':userForm,'clientForm':clientForm}
     
#     if request.method=='POST':
        
#         userForm=forms.ClientUserForm(request.POST)
#         clientForm=forms.ClientForm(request.POST,request.FILES)
#         print('patient1')
#         if userForm.is_valid() and clientForm.is_valid():
#             print('patient2')
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             print('patient3')
#             client=clientForm.save(commit=False)
#             client.user=user
#             client.assignedLawyerId=request.POST.get('assignedLawyerId')
#             client=client.save()
#             my_client_group = Group.objects.get_or_create(name='CLIENT')
#             my_client_group[0].user_set.add(user)
        

#         return HttpResponseRedirect('clientlogin')
#     else:
        
#         print('patient4')
#     return render(request,'lawfirm/clientsignup.html',context=mydict)



def client_signup_view(request):
    userForm=forms.ClientUserForm()
    clientForm=forms.ClientForm()
    mydict={'userForm':userForm,'clientForm':clientForm}
    if request.method=='POST':
        
        userForm=forms.ClientUserForm(request.POST)
        clientForm=forms.ClientForm(request.POST,request.FILES)
        print("Client1")
        print(clientForm.is_valid(), clientForm.errors, type(clientForm.errors))
        if userForm.is_valid() and clientForm.is_valid():
            print("Client2")
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            client=clientForm.save(commit=False)
            client.user=user
            client.assignedLawyerId=request.POST.get('assignedLawyerId')
            client=client.save()
            
            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)
        return HttpResponseRedirect('clientlogin')
    return render(request,'lawfirm/clientsignup.html',context=mydict)




#-----------for checking user is lawyer , client or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_lawyer(user):
    return user.groups.filter(name='LAWYER').exists()
def is_client(user):
    return user.groups.filter(name='CLIENT').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,LAWYER OR CLIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    
    elif is_lawyer(request.user):
        accountapproval=models.Lawyer.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('lawyer-dashboard')
        else:
            return render(request,'lawfirm/lawyer_wait_for_approval.html')
        
    elif is_client(request.user):
        accountapproval=models.Client.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('client-dashboard')
        else:
            return render(request,'lawfirm/client_wait_for_approval.html')








#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    lawyers=models.Lawyer.objects.all().order_by('-id')
    clients=models.Client.objects.all().order_by('-id')
    #for three cards
    lawyercount=models.Lawyer.objects.all().filter(status=True).count()
    pendinglawyercount=models.Lawyer.objects.all().filter(status=False).count()

    clientcount=models.Client.objects.all().filter(status=True).count()
    pendingclientcount=models.Client.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'lawyers':lawyers,
    'clients':clients,
    'lawyercount':lawyercount,
    'pendinglawyercount':pendinglawyercount,
    'clientcount':clientcount,
    'pendingclientcount':pendingclientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'lawfirm/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_lawyer_view(request):
    return render(request,'lawfirm/admin_lawyer.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_lawyer_view(request):
    lawyers=models.Lawyer.objects.all().filter(status=True)
    return render(request,'lawfirm/admin_view_lawyer.html',{'lawyers':lawyers})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_lawyer_from_lawfirm_view(request,pk):
    lawyer=models.Lawyer.objects.get(id=pk)
    user=models.User.objects.get(id=lawyer.user_id)
    user.delete()
    lawyer.delete()
    return redirect('admin-view-lawyer')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_lawyer_view(request,pk):
    lawyer=models.Lawyer.objects.get(id=pk)
    user=models.User.objects.get(id=lawyer.user_id)

    userForm=forms.LawyerUserForm(instance=user)
    lawyerForm=forms.LawyerForm(request.FILES,instance=lawyer)
    mydict={'userForm':userForm,'lawyerForm':lawyerForm}
    if request.method=='POST':
        userForm=forms.LawyerUserForm(request.POST,instance=user)
        lawyerForm=forms.LawyerForm(request.POST,request.FILES,instance=lawyer)
        if userForm.is_valid() and lawyerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            lawyer=lawyerForm.save(commit=False)
            lawyer.status=True
            lawyer.save()
            return redirect('admin-view-lawyer')
    return render(request,'lawfirm/admin_update_lawyer.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_lawyer_view(request):
    userForm=forms.LawyerUserForm()
    lawyerForm=forms.LawyerForm()
    mydict={'userForm':userForm,'lawyerForm':lawyerForm}
    if request.method=='POST':
        userForm=forms.LawyerUserForm(request.POST)
        lawyerForm=forms.LawyerForm(request.POST, request.FILES)
        if userForm.is_valid() and lawyerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            lawyer=lawyerForm.save(commit=False)
            lawyer.user=user
            lawyer.status=True
            lawyer.save()

            my_lawyer_group = Group.objects.get_or_create(name='LAWYER')
            my_lawyer_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-lawyer')
    return render(request,'lawfirm/admin_add_lawyer.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_lawyer_view(request):
    #those whose approval are needed
    lawyers=models.Lawyer.objects.all().filter(status=False)
    return render(request,'lawfirm/admin_approve_lawyer.html',{'lawyers':lawyers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_lawyer_view(request,pk):
    lawyer=models.Lawyer.objects.get(id=pk)
    lawyer.status=True
    lawyer.save()
    return redirect(reverse('admin-approve-lawyer'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_lawyer_view(request,pk):
    lawyer=models.Lawyer.objects.get(id=pk)
    user=models.User.objects.get(id=lawyer.user_id)
    user.delete()
    lawyer.delete()
    return redirect('admin-approve-lawyer')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_lawyer_specialisation_view(request):
    lawyers=models.Lawyer.objects.all().filter(status=True)
    return render(request,'lawfirm/admin_view_lawyer_specialisation.html',{'lawyers':lawyers})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_client_view(request):
    return render(request,'lawfirm/admin_client.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_client_view(request):
    clients=models.Client.objects.all().filter(status=True)
    return render(request,'lawfirm/admin_view_client.html',{'clients':clients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_client_from_lawfirm_view(request,pk):
    client=models.Client.objects.get(id=pk)
    user=models.User.objects.get(id=client.user_id)
    user.delete()
    client.delete()
    return redirect('admin-view-client')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_client_view(request,pk):
    client=models.Client.objects.get(id=pk)
    user=models.User.objects.get(id=client.user_id)

    userForm=forms.ClientUserForm(instance=user)
    clientForm=forms.ClientForm(request.FILES,instance=client)
    mydict={'userForm':userForm,'clientForm':clientForm}
    if request.method=='POST':
        userForm=forms.ClientUserForm(request.POST,instance=user)
        clientForm=forms.ClientForm(request.POST,request.FILES,instance=client)
        if userForm.is_valid() and clientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            client=clientForm.save(commit=False)
            client.status=True
            client.assignedLawyerId=request.POST.get('assignedLawyerId')
            client.save()
            return redirect('admin-view-client')
    return render(request,'lawfirm/admin_update_client.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_client_view(request):
    userForm=forms.ClientUserForm()
    clientForm=forms.ClientForm()
    mydict={'userForm':userForm,'clientForm':clientForm}
    if request.method=='POST':
        userForm=forms.ClientUserForm(request.POST)
        clientForm=forms.ClientForm(request.POST,request.FILES)
        if userForm.is_valid() and clientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            client=clientForm.save(commit=False)
            client.user=user
            client.status=True
            client.assignedLawyerId=request.POST.get('assignedLawyerId')
            client.save()

            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-client')
    return render(request,'lawfirm/admin_add_client.html',context=mydict)



#------------------FOR APPROVING CLIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_client_view(request):
    #those whose approval are needed
    clients=models.Client.objects.all().filter(status=False)
    return render(request,'lawfirm/admin_approve_client.html',{'clients':clients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_client_view(request,pk):
    client=models.Client.objects.get(id=pk)
    client.status=True
    client.save()
    return redirect(reverse('admin-approve-client'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_client_view(request,pk):
    client=models.Client.objects.get(id=pk)
    user=models.User.objects.get(id=client.user_id)
    user.delete()
    client.delete()
    return redirect('admin-approve-client')



#--------------------- FOR DISCHARGING CLIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_client_view(request):
    clients=models.Client.objects.all().filter(status=True)
    return render(request,'lawfirm/admin_discharge_client.html',{'clients':clients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_client_view(request,pk):
    client=models.Client.objects.get(id=pk)
    days=(date.today()-client.complaintDate) #2 days, 0:00:00
    assignedLawyer=models.User.objects.all().filter(id=client.assignedLawyerId)
    d=days.days # only how many day that is 2
    clientDict={
        'clientId':pk,
        'name':client.get_name,
        'mobile':client.mobile,
        'address':client.address,
        'case_complaint':client.case_complaint,
        'complaintDate':client.complaintDate,
        'todayDate':date.today(),
        'day':d,
        'assignedLawyerName':assignedLawyer[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'hoursCharge':int(request.POST['hoursCharge'])*int(d),
            'lawyerFee':request.POST['lawyerFee'],
            'resourceCost' : request.POST['resourceCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['hoursCharge'])*int(d))+int(request.POST['lawyerFee'])+int(request.POST['resourceCost'])+int(request.POST['OtherCharge'])
        }
        clientDict.update(feeDict)
        #for updating to database clientDischargeDetails (pDD)
        cDD=models.ClientDischargeDetails()
        cDD.clientId=pk
        cDD.clientName=client.get_name
        cDD.assignedlawyerName=assignedLawyer[0].first_name
        cDD.address=client.address
        cDD.mobile=client.mobile
        cDD.case_complaints=client.case_complaint
        cDD.complaintDate=client.complaintDate
        cDD.releaseDate=date.today()
        cDD.daySpent=int(d)
        cDD.resourceCost=int(request.POST['resourceCost'])
        cDD.hoursCharge=int(request.POST['hoursCharge'])*int(d)
        cDD.lawyerFee=int(request.POST['lawyerFee'])
        cDD.OtherCharge=int(request.POST['OtherCharge'])
        cDD.total=(int(request.POST['hoursCharge'])*int(d))+int(request.POST['lawyerFee'])+int(request.POST['resourceCost'])+int(request.POST['OtherCharge'])
        cDD.save()
        return render(request,'lawfirm/client_final_bill.html',context=clientDict)
    return render(request,'lawfirm/client_generate_bill.html',context=clientDict)



#--------------for discharge client bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse



def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.ClientDischargeDetails.objects.all().filter(clientId=pk).order_by('-id')[:1]
    dict={
        'clientName':dischargeDetails[0].clientName,
        'assignedLawyerName':dischargeDetails[0].assignedlawyerName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'case_complaints':dischargeDetails[0].case_complaints,
        'complaintDate':dischargeDetails[0].complaintDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'resourceCost':dischargeDetails[0].resourceCost,
        'hoursCharge':dischargeDetails[0].hoursCharge,
        'lawyerFee':dischargeDetails[0].lawyerFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('lawfirm/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'lawfirm/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'lawfirm/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.lawyerId=request.POST.get('lawyerId')
            appointment.clientId=request.POST.get('clientId')
            appointment.lawyerName=models.User.objects.get(id=request.POST.get('lawyerId')).first_name
            appointment.clientName=models.User.objects.get(id=request.POST.get('clientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'lawfirm/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'lawfirm/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ LAWYER RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='lawyerlogin')
@user_passes_test(is_lawyer)
def lawyer_dashboard_view(request):
    #for three cards
    clientcount=models.Client.objects.all().filter(status=True,assignedLawyerId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,lawyerId=request.user.id).count()
    clientdischarged=models.ClientDischargeDetails.objects.all().distinct().filter(assignedlawyerName=request.user.first_name).count()

    #for  table in Lawyer dashboard
    appointments=models.Appointment.objects.all().filter(status=True,lawyerId=request.user.id).order_by('-id')
    clientid=[]
    for a in appointments:
        clientid.append(a.clientId)
    clients=models.Client.objects.all().filter(status=True,user_id__in=clientid).order_by('-id')
    appointments=zip(appointments,clients)
    mydict={
    'clientcount':clientcount,
    'appointmentcount':appointmentcount,
    'clientdischarged':clientdischarged,
    'appointments':appointments,
    # 'lawyer':models.Lawyer.objects.get(user_id=request.user.id), #for profile picture of lawyer in sidebar
    }
    return render(request,'lawfirm/lawyer_dashboard.html',context=mydict)



@login_required(login_url='lawyerlogin')
@user_passes_test(is_lawyer)
def lawyer_client_view(request):
    mydict={
    'lawyer':models.Lawyer.objects.get(user_id=request.user.id), #for profile picture of lawyer in sidebar
    }
    return render(request,'lawfirm/lawyer_client.html',context=mydict)



@login_required(login_url='lawyerlogin')
@user_passes_test(is_lawyer)
def lawyer_view_client_view(request):
    clients=models.Client.objects.all().filter(status=True,assignedLawyerId=request.user.id)
    lawyer=models.Lawyer.objects.get(user_id=request.user.id) #for profile picture of lawyer in sidebar
    return render(request,'lawfirm/lawyer_view_client.html',{'clients':clients,'lawyer':lawyer})



@login_required(login_url='lawyerlogin')
@user_passes_test(is_lawyer)
def lawyer_view_discharge_client_view(request):
    dischargedclients=models.ClientDischargeDetails.objects.all().distinct().filter(assignedlawyerName=request.user.first_name)
    lawyer=models.Lawyer.objects.get(user_id=request.user.id) #for profile picture of lawyer in sidebar
    return render(request,'lawfirm/lawyer_view_discharge_client.html',{'dischargedclients':dischargedclients,'lawyer':lawyer})



@login_required(login_url='lawyerlogin')
@user_passes_test(is_lawyer)
def lawyer_appointment_view(request):
    lawyer=models.Lawyer.objects.get(user_id=request.user.id) #for profile picture of lawyer in sidebar
    return render(request,'lawfirm/lawyer_appointment.html',{'lawyer':lawyer})



@login_required(login_url='lawyerlogin')
@user_passes_test(is_lawyer)
def lawyer_view_appointment_view(request):
    lawyer=models.Lawyer.objects.get(user_id=request.user.id) #for profile picture of lawyer in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,lawyerId=request.user.id)
    clientid=[]
    for a in appointments:
        clientid.append(a.clientId)
    clients=models.Client.objects.all().filter(status=True,user_id__in=clientid)
    appointments=zip(appointments,clients)
    return render(request,'lawfirm/lawyer_view_appointment.html',{'appointments':appointments,'lawyer':lawyer})



@login_required(login_url='lawyerlogin')
@user_passes_test(is_lawyer)
def lawyer_delete_appointment_view(request):
    lawyer=models.Lawyer.objects.get(user_id=request.user.id) #for profile picture of lawyer in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,lawyerId=request.user.id)
    clientid=[]
    for a in appointments:
        clientid.append(a.clientId)
    clients=models.Client.objects.all().filter(status=True,user_id__in=clientid)
    appointments=zip(appointments,clients)
    return render(request,'lawfirm/lawyer_delete_appointment.html',{'appointments':appointments,'lawyer':lawyer})



@login_required(login_url='lawyerlogin')
@user_passes_test(is_lawyer)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    lawyer=models.Lawyer.objects.get(user_id=request.user.id) #for profile picture of lawyer in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,lawyerid=request.user.id)
    clientid=[]
    for a in appointments:
        clientid.append(a.clientId)
    clients=models.Client.objects.all().filter(status=True,user_id__in=clientid)
    appointments=zip(appointments,clients)
    return render(request,'lawfirm/lawyer_delete_appointment.html',{'appointments':appointments,'lawyer':lawyer})



#---------------------------------------------------------------------------------
#------------------------ Lawyer RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ Client RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_dashboard_view(request):
    client=models.Client.objects.get(user_id=request.user.id)
    lawyer=models.Lawyer.objects.get(user_id=client.assignedLawyerId)
    mydict={
    'client':client,
    'lawyerName':lawyer.get_name,
    'lawyerMobile':lawyer.mobile,
    'lawyerAddress':lawyer.address,
    'case_complaint':client.case_complaint,
    'lawyerDepartment':lawyer.department,
    'complaintDate':client.complaintDate,
    }
    return render(request,'lawfirm/client_dashboard.html',context=mydict)



@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_appointment_view(request):
    client=models.Client.objects.get(user_id=request.user.id) #for profile picture of client in sidebar
    return render(request,'lawfirm/client_appointment.html',{'client':client})



@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_book_appointment_view(request):
    appointmentForm=forms.ClientAppointmentForm()
    client=models.Client.objects.get(user_id=request.user.id) #for profile picture of Client in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'client':client,'message':message}
    if request.method=='POST':
        appointmentForm=forms.ClientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('lawyerId'))
            desc=request.POST.get('description')

            lawyer=models.Lawyer.objects.get(user_id=request.POST.get('lawyerId'))
            
            if lawyer.department == 'Bankruptcy Lawyer':
                if 'consumer bankruptcy or commercial bankruptcy.' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose a Lawyer According To Case"
                    return render(request,'lawfirm/client_book_appointment.html',{'appointmentForm':appointmentForm,'client':client,'message':message})


            if lawyer.department == 'Business Lawyer (Corporate Lawyer)':
                if 'business' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Lawyer According To Case"
                    return render(request,'lawfirm/client_book_appointment.html',{'appointmentForm':appointmentForm,'client':client,'message':message})

            if lawyer.department == 'Constitutional Lawyer':
                if 'Constitution' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Lawyer According To Case"
                    return render(request,'lawfirm/client_book_appointment.html',{'appointmentForm':appointmentForm,'client':client,'message':message})

            if lawyer.department == 'Criminal Defense Lawyer':
                if 'Crime' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Lawyer According To Case"
                    return render(request,'lawfirm/client_book_appointment.html',{'appointmentForm':appointmentForm,'client':client,'message':message})

            if lawyer.department == 'Employment and Labor Lawyer':
                if 'Employee' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Lawyer According To Case"
                    return render(request,'lawfirm/client_book_appointment.html',{'appointmentForm':appointmentForm,'client':client,'message':message})

            if lawyer.department == 'Entertainment Lawyer':
                if 'entertainment' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Lawyer According To Case"
                    return render(request,'lawfirm/client_book_appointment.html',{'appointmentForm':appointmentForm,'client':client,'message':message})





            appointment=appointmentForm.save(commit=False)
            appointment.lawyerId=request.POST.get('lawyerId')
            appointment.clientId=request.user.id #----user can choose any client but only their info will be stored
            appointment.lawyerName=models.User.objects.get(id=request.POST.get('lawyerId')).first_name
            appointment.clientName=request.user.first_name #----user can choose any client but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('client-view-appointment')
    return render(request,'lawfirm/client_book_appointment.html',context=mydict)





@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_view_appointment_view(request):
    client=models.Client.objects.get(user_id=request.user.id) #for profile picture of client in sidebar
    appointments=models.Appointment.objects.all().filter(clientId=request.user.id)
    return render(request,'lawfirm/client_view_appointment.html',{'appointments':appointments,'client':client})



@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_discharge_view(request):
    client=models.Client.objects.get(user_id=request.user.id) #for profile picture of client in sidebar
    dischargeDetails=models.ClientDischargeDetails.objects.all().filter(clientId=client.id).order_by('-id')[:1]
    clientDict=None
    if dischargeDetails:
        clientDict ={
        'is_discharged':True,
        'client':client,
        'clientId':client.id,
        'clientName':client.get_name,
        'assignedLawyerName':dischargeDetails[0].assignedlawyerName,
        'address':client.address,
        'mobile':client.mobile,
        'case_complaint':client.case_complaint,
        'complaintDate':client.complaintDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'resourceCost':dischargeDetails[0].resourceCost,
        'hoursCharge':dischargeDetails[0].hoursCharge,
        'lawyerFee':dischargeDetails[0].lawyerFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(clientDict)
    else:
        clientDict={
            'is_discharged':False,
            'client':client,
            'clientId':request.user.id,
        }
    return render(request,'lawfirm/client_discharge.html',context=clientDict)


#------------------------ LAwyer RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'lawfirm/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'lawfirm/contactussuccess.html')
    return render(request, 'lawfirm/contactus.html', {'form':sub})

