
from django.urls import path
from . import views

urlpatterns = [
   path('create/',views.create,name='create'),
   path('userview/',views.userview,name='userview'),
    path('doctorview/',views.doctorview,name='doctorview'),
    path('create_doctor/',views.create_doctor,name='create_doctor'),


    path('appointment/',views.appointment,name='appointment'),
    path('success/',views.payment_success,name='success'),
    path('cancel/',views.payment_cancel,name='cancel'),
    path('payment_session/',views.payment_session,name='payment_session'),


    path('appointment_option/',views.appointments_option,name='appointments'),
    path('update/<int:id>/',views.update_appointment,name='update'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('appointmentdetails/',views.appointment_details,name='list'),
    path('detail/<int:id>/',views.detail,name='detail'),
    path('details/',views.details,name='details'),
    path('medical_history/<int:appointment_id>/',views.medical_create,name='medical'),
    path('medical_details/',views.medical_details,name='medical_details'),
    path('medical_all/<int:id>/',views.update_medical_show,name='medical_show'),
    path('medical_update/<int:id>/',views.medical_update,name='medical_update'),
    path('medical_delete/<int:id>/',views.medical_delete,name='medical_delete'),
    path('prescription_create/',views.prescription,name='prescription'),
    path('prescription_list/',views.prescription_list,name='prescription_list'),
    path('health_resource/',views.healthview,name='health'),
    path('tips/',views.healthtips,name='tips'),
    path('prevention/',views.prevention,name='prevention'),
    path('resource/',views.resource,name='resource'),

    path('admin/',views.adminview,name='admin'),
    path('user_list/',views.user_list,name='user_list'),
    path('user_update/<int:id>/',views.user_update,name='user_update'),
    path('user_delete/<int:id>/',views.user_delete,name='user_delete'),
    path('facility_options/',views.manage_facility,name='manage'),
    path('location_create/',views.location_create,name='location_create'),
        path('location_update/<int:id>/',views.location_update,name='location_update'),
            path('location_delete/<int:id>/',views.location_delete,name='location_delete'),

                path('dept_create/',views.dept_create,name='dept_create'),
        path('dept_update/<int:id>/',views.dept_update,name='dept_update'),
            path('dept_delete/<int:id>/',views.dept_delete,name='dept_delete'),

                 path('res_create/',views.res_create,name='res_create'),
        path('res_update/<int:id>/',views.res_update,name='res_update'),
            path('res_delete/<int:id>/',views.res_delete,name='res_delete'),

            path('appointment_show/',views.appointment_show,name='appointment_show'),

            path('appointment_update/<int:id>/',views.appo_update,name='appo_update'),
            path('appointment_delete/<int:id>/',views.appo_delete,name='appo_delete')
 
]
