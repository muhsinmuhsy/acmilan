from django.urls import path
from . import views


urlpatterns = [

    # ------------------------------------------- Auth --------------------------------------------------------- #
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ------------------------------------------- Index --------------------------------------------------------- #

    path('', views.dashbord, name='dashbord'),

    # ------------------------------------------- Centers ------------------------------------------------------- #

    path('centers/', views.center_list, name='center_list'),
    path('centers/add/', views.center_add, name='center_add'),
    path('centers/<int:center_id>/edit/', views.center_edit, name='center_edit'),
    path('centers/<int:center_id>/delete/', views.center_delete, name='center_delete'),
    path('center_student_list/<int:center_id>/', views.center_student_list, name='center_student_list'),
    path('delete-student/<int:student_id>/', views.center_delete_student, name='center_delete_student'),

    # ------------------------------------------- Corrdinators ------------------------------------------------- #

    path('coordinators/', views.coordinator_list, name='coordinator_lists'),
    path('add_coordinator/', views.add_coordinator, name='add_coordinator'),
    path('coordinator/<int:coordinator_id>/edit/', views.edit_coordinator, name='edit_coordinator'),
    path('delete-coordinator/<int:coordinator_id>/', views.delete_coordinator, name='delete_coordinator'),

    # -------------------------------------------- leads ------------------------------------------------------ #

    path('add_lead', views.add_lead, name='add_lead'),
    path('lead_list', views.lead_list, name='lead_list'),
    path('leads/<int:lead_id>/delete/', views.delete_lead, name='delete_lead'),
    path('lead_view/<int:lead_id>', views.lead_view, name='lead_view'),

    # ------------------------------------------- Students ------------------------------------------------------ #

    path('student_list', views.student_list, name='student_list'),
    path('add_student/<int:center_id>', views.add_student, name='add_student'),
    path('student/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('view-student/<int:student_id>/', views.view_student, name='view_student'),

    # ------------------------------------------ Attendance ------------------------------------------------------- #

    # Centers
    path('attends_center/', views.attends_centers, name='attends_centers'),

    # Batches
    path('center_batch/<int:center_id>/', views.center_batch, name='center_batch'),

    # Timesections
    path('centers/<int:center_id>/<int:batch_id>/', views.batch_sections, name='batch_sections'),
    path('add_time_section/<int:center_id>/<int:batch_id>', views.add_time_section, name='add_time_section'),
    path('update_time_section/<int:center_id>/<int:batch_id>/<int:section_id>', views.update_time_section, name='update_time_section'),
    path('delete_section/<int:center_id>/<int:batch_id>/<int:section_id>/', views.delete_section, name='delete_section'),

    # Attends
    path('attendance_date/<int:center_id>/<int:batch_id>/<int:section_id>/', views.attendance_date, name='attendance_date'),
    path('attendance_date/<int:center_id>/<int:batch_id>/<int:section_id>/<str:date>/delete/', views.delete_attendance_date, name='delete_attendance_date'),
    path('centers/<int:center_id>/timesections/<int:batch_id>/<int:section_id>/addattendance/', views.add_attendance, name='add_attendance'),
    # path('center/<int:center_id>/section/<int:section_id>/attendance/<int:attendance_id>/edit/', views.edit_attendance, name='edit_attendance'),      
    path('center/<int:center_id>/batch/<int:batch_id>/<int:section_id>/attendance-date/<str:date>/', views.attendance_detail, name='attendance_detail'),
    
    
    
]


