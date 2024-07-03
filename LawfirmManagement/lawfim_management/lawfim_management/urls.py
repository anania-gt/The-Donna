"""lawfim_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from lawfirm import views
from django.contrib.auth.views import LoginView,LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),


    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),


    path('adminclick', views.adminclick_view),
    path('lawyerclick', views.lawyerclick_view),
    path('clientclick', views.clientclick_view),

    path('adminsignup', views.admin_signup_view),
    path('lawyersignup', views.lawyer_signup_view,name='lawyersignup'),
    path('clientsignup', views.client_signup_view),
    
    path('adminlogin', LoginView.as_view(template_name='lawfirm/adminlogin.html')),
    path('lawyerlogin', LoginView.as_view(template_name='lawfirm/lawyerlogin.html')),
    path('clientlogin', LoginView.as_view(template_name='lawfirm/clientlogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='lawfirm/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-lawyer', views.admin_lawyer_view,name='admin-lawyer'),
    path('admin-view-lawyer', views.admin_view_lawyer_view,name='admin-view-lawyer'),
    path('delete-lawyer-from-lawfirm/<int:pk>', views.delete_lawyer_from_lawfirm_view,name='delete-lawyer-from-lawfirm'),
    path('update-lawyer/<int:pk>', views.update_lawyer_view,name='update-lawyer'),
    path('admin-add-lawyer', views.admin_add_lawyer_view,name='admin-add-lawyer'),
    path('admin-approve-lawyer', views.admin_approve_lawyer_view,name='admin-approve-lawyer'),
    path('approve-lawyer/<int:pk>', views.approve_lawyer_view,name='approve-lawyer'),
    path('reject-lawyer/<int:pk>', views.reject_lawyer_view,name='reject-lawyer'),
    path('admin-view-lawyer-specialisation',views.admin_view_lawyer_specialisation_view,name='admin-view-lawyer-specialisation'),


    path('admin-client', views.admin_client_view,name='admin-client'),
    path('admin-view-client', views.admin_view_client_view,name='admin-view-client'),
    path('delete-client-from-lawfirm/<int:pk>', views.delete_client_from_lawfirm_view,name='delete-client-from-lawfirm'),
    path('update-client/<int:pk>', views.update_client_view,name='update-client'),
    path('admin-add-client', views.admin_add_client_view,name='admin-add-client'),
    path('admin-approve-client', views.admin_approve_client_view,name='admin-approve-client'),
    path('approve-client/<int:pk>', views.approve_client_view,name='approve-client'),
    path('reject-client/<int:pk>', views.reject_client_view,name='reject-client'),
    path('admin-discharge-client', views.admin_discharge_client_view,name='admin-discharge-client'),
    path('discharge-client/<int:pk>', views.discharge_client_view,name='discharge-client'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),



    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]

#---------FOR LAWYER RELATED URLS-------------------------------------
urlpatterns +=[
    path('lawyer-dashboard', views.lawyer_dashboard_view,name='lawyer-dashboard'),

    path('lawyer-client', views.lawyer_client_view,name='lawyer-client'),
    path('lawyer-view-client', views.lawyer_view_client_view,name='lawyer-view-client'),
    path('lawyer-view-discharge-client',views.lawyer_view_discharge_client_view,name='lawyer-view-discharge-client'),

    path('lawyer-appointment', views.lawyer_appointment_view,name='lawyer-appointment'),
    path('lawyer-view-appointment', views.lawyer_view_appointment_view,name='lawyer-view-appointment'),
    path('lawyer-delete-appointment',views.lawyer_delete_appointment_view,name='lawyer-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
]




#---------FOR CLIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('client-dashboard', views.client_dashboard_view,name='client-dashboard'),
    path('client-appointment', views.client_appointment_view,name='client-appointment'),
    path('client-book-appointment', views.client_book_appointment_view,name='client-book-appointment'),
    path('client-view-appointment', views.client_view_appointment_view,name='client-view-appointment'),
    path('client-discharge', views.client_discharge_view,name='client-discharge'),

]