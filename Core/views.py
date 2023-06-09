from django.shortcuts import render, redirect
from .models import *
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


# Create your models here.

# ---------------------------------------- Auth --------------------------------------------------------#
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('dashbord')
#         else:
#             error = 'Invalid username or password. Please try again.'
#     else:
#         error = None
#     return render(request, 'login.html', {'error': error})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the login time
            user.last_login = timezone.now()
            user.save()

            login(request, user)
            return redirect('dashbord')
        else:
            error = 'Invalid username or password. Please try again.'
    else:
        error = None
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('dashbord')

# ------------------------------------- Index --------------------------------------------------- #

# @login_required 
# def dashbord(request):
#     center_count = Center.objects.count()
#     coordianator_count = Coordinator.objects.count()
#     student_count = Student.objects.count()
#     # student_count = Student.objects.annotate(num_students=Count('id'))
#     return render(request, 'dashbord.html', {'student_count': student_count, 'center_count':center_count, 'coordinator_count':coordianator_count})

@login_required
def dashbord(request):
    center_count = Center.objects.count()
    coordianator_count = Coordinator.objects.count()
    student_count = Student.objects.count()

    # Get a list of all users and their last login times
    users = User.objects.all().order_by('-last_login')[:10]
    user_logins = [(u.username, u.last_login.astimezone(timezone.get_current_timezone()) if u.last_login is not None else None) for u in users]

     # get the latest 5 student added logs
    added_students = StudentAddedLog.objects.order_by('-date_added')[:5]
    added_student_details = [(log.student_name, log.date_added, log.added_by.username) for log in added_students]
    return render(request, 'dashbord.html', {
        'user_logins': user_logins,
        'student_count': student_count,
        'center_count': center_count,
        'coordinator_count': coordianator_count,
        'added_students': added_student_details,
    })

# ---------------------------------- Coordinators -----------------------------------------------------#

@login_required 
def coordinator_list(request):
    coordinators = Coordinator.objects.all()
    return render(request, 'coordinator_lists.html', {'coordinators': coordinators})

@login_required 
def add_coordinator(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        center1_id = request.POST['center1']
        center2_id = request.POST['center2']
        primary_mobile = request.POST['primary_mobile']
        secondary_mobile = request.POST['secondary_mobile']
        place = request.POST['place']
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, is_staff=True)
            center1 = get_object_or_404(Center, id=center1_id)
            center2 = get_object_or_404(Center, id=center2_id)
            coordinator = Coordinator.objects.create(user=user, primary_mobile=primary_mobile, secondary_mobile=secondary_mobile, place=place)
            coordinator.centers.add(center1, center2)
            return redirect('coordinator_lists')
        except IntegrityError:
            message = f"The username '{username}' is already taken. Please choose a different username."
            centers = Center.objects.all()
            return render(request, 'add_coordinator.html', {'centers': centers, 'message': message})
    else:
        centers = Center.objects.all()
        return render(request, 'add_coordinator.html', {'centers': centers})

@login_required     
def edit_coordinator(request, coordinator_id):
    coordinator = get_object_or_404(Coordinator, id=coordinator_id)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        center1_id = request.POST['center1']
        center2_id = request.POST['center2']
        primary_mobile = request.POST['primary_mobile']
        secondary_mobile = request.POST['secondary_mobile']
        place = request.POST['place']
        
        try:
            user = coordinator.user
            user.username = username
            user.email = email
            if password:
                user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            coordinator.primary_mobile = primary_mobile
            coordinator.secondary_mobile = secondary_mobile
            coordinator.place = place
            
            # Clear the existing centers and add the updated ones
            coordinator.centers.clear()
            center1 = get_object_or_404(Center, id=center1_id)
            center2 = get_object_or_404(Center, id=center2_id)
            coordinator.centers.add(center1, center2)
            coordinator.save()
            
            # Redirect to the coordinator list page
            return redirect('coordinator_lists')
        except IntegrityError:
            message = f"The username '{username}' is already taken. Please choose a different username."
            centers = Center.objects.all()
            return render(request, 'edit_coordinator.html', {'coordinator': coordinator, 'centers': centers, 'message': message})
    else:
        centers = Center.objects.all()
        return render(request, 'edit_coordinator.html', {'coordinator': coordinator, 'centers': centers})

@login_required 
def delete_coordinator(request, coordinator_id):
    coordinator = Coordinator.objects.get(pk=coordinator_id)
    coordinator.delete()
    return redirect('coordinator_lists')

# ------------------------------------- Centers --------------------------------------------------------------- #

# @login_required 
# def center_list(request):
#     if request.user.is_superuser:
#         centers = Center.objects.annotate(student_count=Count('student'))
#     else:
#         coordinator = Coordinator.objects.get(user=request.user)
#         centers = coordinator.centers.all()
#     return render(request, 'center_list.html', {'centers': centers})

@login_required
def center_list(request):
    if request.user.is_superuser:
        # if user is a superuser, show all centers
        centers = Center.objects.annotate(student_count=Count('student'))
    else:
        # if user is a coordinator, show only their associated centers
        coordinator = request.user.coordinator
        centers = coordinator.centers.annotate(student_count=Count('student'))

    return render(request, 'center_list.html', {'centers': centers})


@login_required 
def center_add(request):
    if request.method == 'POST':
        ref_number = request.POST['ref_number']
        name = request.POST['name']
        location = request.POST['location']
        address = request.POST['address']
        center = Center(ref_number=ref_number, name=name, location=location, address=address)
        try:
            center.save()
        except IntegrityError:
            messages.error(request, 'Ref number already exists.')
            return redirect('center_add')
        else:
            return redirect('center_list')
    return render(request, 'center_add.html')

def center_edit(request, center_id):
    center = Center.objects.get(pk=center_id)
    if request.method == 'POST':
        ref_number = request.POST['ref_number']
        name = request.POST['name']
        location = request.POST['location']
        address = request.POST['address']
        center.ref_number = ref_number
        center.name = name
        center.location = location
        center.address = address
        try:
            center.save()
        except IntegrityError:
            messages.error(request, 'Ref number already exists.')
            return redirect('center_edit', center_id=center.id)
        else:
            return redirect('center_list')
    return render(request, 'center_edit.html', {'center': center})

@login_required 
def center_delete(request, center_id):
    center = Center.objects.get( pk=center_id)
    center.delete()
    return redirect('center_list')

def center_student_list(request, center_id):
    center = Center.objects.get(id=center_id)
    students = Student.objects.filter(center=center)
    return render(request, 'center_student_list.html', {'center': center, 'students': students})

def center_delete_student(request, student_id):
    student = Student.objects.get(pk=student_id)
    student.delete()
    return redirect('center_student_list', center_id=student.center.id)

# ---------------------------------------- Leads ---------------------------------------------------- #

@login_required
def add_lead(request):
    lead_types = Lead.LEAD_TYPES
    
    if request.user.is_superuser:
        coordinators = Coordinator.objects.all()
    else:
        coordinators = [request.user.coordinator]  # Only show current user's coordinator
        
    if request.method == 'POST':
        ref_no = request.POST.get('ref_no')
        student_name = request.POST.get('student_name')
        guardian_name = request.POST.get('guardian_name')
        contact_no = request.POST.get('contact_no')
        location = request.POST.get('location')
        coordiantor_id = request.POST.get('coordinator')
        coordiantor = get_object_or_404(Coordinator, id=coordiantor_id)
        lead_type = request.POST.get('lead_type')
        
        lead = Lead.objects.create(
            ref_no=ref_no,
            student_name=student_name,
            guardian_name=guardian_name,
            contact_no=contact_no,
            location=location,
            coordinator=coordiantor,
            lead_type=lead_type,
        )
        lead.save()
        return redirect('lead_list')
    else:
        return render(request, 'add_lead.html', {'coordinators': coordinators, 'lead_types': lead_types})


@login_required
def lead_list(request):
    if request.user.is_superuser:
        # If the user is an admin, show all leads
        leads = Lead.objects.all()
    else:
        # If the user is a coordinator, show only their assigned leads
        leads = Lead.objects.filter(coordinator=request.user.coordinator)

    return render(request, 'lead_list.html', {'leads': leads})


@login_required 
def delete_lead(request, lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)
    lead.delete()
    return redirect('lead_list')

@login_required 
def lead_view(request, lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update':
            comment = request.POST.get('comment')
            lead.comment = comment
            lead.save()
        elif action == 'reject':
            lead.lead_status = 'Rejected'
            lead.save()
        elif action == 'success':
            lead.lead_status = 'Success'
            lead.save()
            return redirect('lead_student')
        elif action == 'pending':
            lead.lead_status = 'Pending'
            lead.save()

    return render(request, 'lead_view.html', {'lead': lead, 'comment': lead.comment})



def lead_student(request):
    message = None
    centers = Center.objects.all()
    if request.method == 'POST':
        center_id = request.POST.get('center')  # get the selected center_id from the form
        center = Center.objects.get(id=center_id)  # retrieve the center instance based on the id
        student = Student(
            ref_number=request.POST['ref_number'],
            full_name=request.POST['full_name'],
            city=request.POST['city'],
            zipcode=request.POST['zipcode'],
            email=request.POST['email'],
            date_of_birth=request.POST['date_of_birth'],
            preferred_location=request.POST['preferred_location'],
            street_address=request.POST['street_address'],
            state=request.POST['state'],
            phone_number=request.POST['phone_number'],
            guardian_name=request.POST['guardian_name'],
            guardian_phone_number=request.POST['guardian_phone_number'],
            id_proof=request.FILES.get('id_proof'),
            age_group=request.POST['age_group'],
            mode_of_travel=request.POST['mode_of_travel'],
            football_playing_position=request.POST['football_playing_position'],
            school_Name=request.POST['school_Name'],
            school_Address=request.POST['school_Address'],
            study_Standard=request.POST['study_Standard'],
            study_Devision=request.POST['study_Devision'],
            center=center,  # assign the center instance, not the id
        )
        try:
            student.save()
            center.num_students += 1
            center.save()

            student_added_log = StudentAddedLog.objects.create(
                added_by=request.user,
                student_name=student.full_name,
                date_added=timezone.now()
            )
            return redirect('center_student_list', center_id=center.id)
        except IntegrityError:
            message = f"A student with this reference number already exists."
    else:
        student = Student()
    return render(request, 'lead_student.html', {'student': student, 'centers': centers, 'message': message})


# ---------------------------------- Students -------------------------------------------------- #

@login_required 
def student_list(request):
    if request.user.is_superuser:
        students = Student.objects.all()
    else:
        coordinator = Coordinator.objects.get(user=request.user)
        centers = coordinator.centers.all()
        students = Student.objects.filter(center__in=centers)
    return render(request, 'student_list.html' ,{'students':students})


# @login_required 
# def add_student(request, center_id):
#     message = None
#     center = Center.objects.get(pk=center_id)
#     batches = center.batch_set.all()
#     if request.method == 'POST':
#         student = Student(
#             ref_number=request.POST['ref_number'],
#             full_name=request.POST['full_name'],
#             city=request.POST['city'],
#             zipcode=request.POST['zipcode'],
#             email=request.POST['email'],
#             date_of_birth=request.POST['date_of_birth'],
#             preferred_location=request.POST['preferred_location'],
#             street_address=request.POST['street_address'],
#             state=request.POST['state'],
#             phone_number=request.POST['phone_number'],
#             guardian_name=request.POST['guardian_name'],
#             guardian_phone_number=request.POST['guardian_phone_number'],
#             id_proof=request.FILES.get('id_proof'),
#             age_group=request.POST['age_group'],
#             mode_of_travel=request.POST['mode_of_travel'],
#             football_playing_position=request.POST['football_playing_position'],
#             school_Name=request.POST['school_Name'],
#             school_Address=request.POST['school_Address'],
#             study_Standard=request.POST['study_Standard'],
#             study_Devision=request.POST['study_Devision'],
#             center=center,
#             batch=Batch.objects.get(pk=request.POST['batch'])
#         )
#         try:
#             student.save()
#             center.num_students += 1
#             center.save()
            
#             return redirect('center_student_list', center_id=center.id)
#         except IntegrityError:
#             message = f"A student with this reference number already exists."
#     else:
        
#         student = Student()
#     return render(request, 'add_student.html', {'student': student, 'center': center, 'batches': batches,'message':message})

@login_required 
def add_student(request, center_id):
    message = None
    center = Center.objects.get(pk=center_id)
    batches = center.batch_set.all()
    if request.method == 'POST':
        student = Student(
            ref_number=request.POST['ref_number'],
            full_name=request.POST['full_name'],
            city=request.POST['city'],
            zipcode=request.POST['zipcode'],
            email=request.POST['email'],
            date_of_birth=request.POST['date_of_birth'],
            preferred_location=request.POST['preferred_location'],
            street_address=request.POST['street_address'],
            state=request.POST['state'],
            phone_number=request.POST['phone_number'],
            guardian_name=request.POST['guardian_name'],
            guardian_phone_number=request.POST['guardian_phone_number'],
            id_proof=request.FILES.get('id_proof'),
            age_group=request.POST['age_group'],
            mode_of_travel=request.POST['mode_of_travel'],
            football_playing_position=request.POST['football_playing_position'],
            school_Name=request.POST['school_Name'],
            school_Address=request.POST['school_Address'],
            study_Standard=request.POST['study_Standard'],
            study_Devision=request.POST['study_Devision'],
            center=center,
            batch=Batch.objects.get(pk=request.POST['batch'])
        )
        try:
            student.save()
            center.num_students += 1
            center.save()
            
            # create and save student added log object
            student_added_log = StudentAddedLog.objects.create(
                added_by=request.user,
                student_name=student.full_name,
                date_added=timezone.now()
            )
            
            return redirect('center_student_list', center_id=center.id)
        except IntegrityError:
            message = f"A student with this reference number already exists."
    else:
        student = Student()
    return render(request, 'add_student.html', {'student': student, 'center': center, 'batches': batches, 'message': message})


# @login_required 
# def edit_student(request, student_id):
#     student = get_object_or_404(Student, id=student_id)
#     if request.method == 'POST':
#         student.ref_number = request.POST['ref_number']
#         student.full_name = request.POST['full_name']
#         student.city = request.POST['city']
#         student.zipcode = request.POST['zipcode']
#         student.email = request.POST['email']
#         student.date_of_birth = request.POST['date_of_birth']
#         student.preferred_location = request.POST['preferred_location']
#         student.street_address = request.POST['street_address']
#         student.state = request.POST['state']
#         student.phone_number = request.POST['phone_number']
#         student.guardian_name = request.POST['guardian_name']
#         student.guardian_phone_number = request.POST['guardian_phone_number']
#         if request.FILES.get('id_proof'):
#             student.id_proof = request.FILES['id_proof']
#         student.age_group = request.POST['age_group']
#         student.mode_of_travel = request.POST['mode_of_travel']
#         student.football_playing_position = request.POST['football_playing_position']
#         student.school_Name = request.POST['school_Name']
#         student.school_Address = request.POST['school_Address']
#         student.study_Standard = request.POST['study_Standard']
#         student.study_Devision = request.POST['study_Devision']
#         student.save()
#         return redirect('center_student_list', center_id=student.center.id)
#     centers = Center.objects.all()
#     return render(request, 'edit_student.html', {'student': student, 'centers': centers})

@login_required 
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.ref_number = request.POST['ref_number']
        student.full_name = request.POST['full_name']
        student.city = request.POST['city']
        student.zipcode = request.POST['zipcode']
        student.email = request.POST['email']
        student.date_of_birth = request.POST['date_of_birth']
        student.preferred_location = request.POST['preferred_location']
        student.street_address = request.POST['street_address']
        student.state = request.POST['state']
        student.phone_number = request.POST['phone_number']
        student.guardian_name = request.POST['guardian_name']
        student.guardian_phone_number = request.POST['guardian_phone_number']
        if request.FILES.get('id_proof'):
            student.id_proof = request.FILES['id_proof']
        student.age_group = request.POST['age_group']
        student.mode_of_travel = request.POST['mode_of_travel']
        student.football_playing_position = request.POST['football_playing_position']
        student.school_Name = request.POST['school_Name']
        student.school_Address = request.POST['school_Address']
        student.study_Standard = request.POST['study_Standard']
        student.study_Devision = request.POST['study_Devision']
        student.batch = Batch.objects.get(pk=request.POST['batch'])
        student.save()
        return redirect('center_student_list', center_id=student.center.id)
    centers = Center.objects.all()
    center = student.center
    batches = center.batch_set.all()
    return render(request, 'edit_student.html', {'student': student, 'centers': centers, 'center': center, 'batches': batches})


@login_required 
def delete_student(request, student_id):
    student = Student.objects.get(pk=student_id)
    student.delete()
    return redirect('student_list')

@login_required 
def view_student(request, student_id):
    student = Student.objects.get(pk=student_id)
    attendance_records = Attendance.objects.filter(Student=student)

    # Payment
    payments = Payment.objects.filter(student=student)

    if request.method == 'POST' :
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        payment = Payment(student=student,date=date,amount=amount,description=description)
        payment.save()
        return redirect('.')
    context = {
        'student': student,
        'attendance_records': attendance_records,
        'payments' : payments,
    }
    return render(request, "view_student.html", context)

@login_required
def delete_payment(request, student_id, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id, student_id=student_id)
    if request.method == 'POST':
        payment.delete()
        return redirect('view_student', student_id=student_id)
    return render(request, 'delete_payment.html', {'payment': payment})

# -------------------------------------- Attendance ---------------------------------------------------- #

# Centers #
@login_required
def attends_centers(request):
    if request.user.is_superuser:
        centers = Center.objects.all()
    else:
        try:
            centers = Center.objects.filter(coordinator=request.user.coordinator)
        except ObjectDoesNotExist:
            centers = Center.objects.none()
        try:
            centers |= Center.objects.filter(coach=request.user.coach)
        except ObjectDoesNotExist:
            pass
    return render(request, "attends_centers.html", {'centers': centers})



# Batches #
@login_required 
def center_batch(request, center_id):
    center = Center.objects.get(pk=center_id)
    batch = Batch.objects.filter(center=center)
    context = {
        'center':center,
        'batch':batch,
    }
    return render(request, 'center_batch.html', context)

# Time section view #
@login_required 
def batch_sections(request, center_id, batch_id):
    center = Center.objects.get(pk=center_id)
    batch = Batch.objects.get(pk=batch_id)
    sections = TimeSection.objects.filter(batch=batch).order_by('-id')
    context = {
        'center': center,
        'batch':batch,
        'sections': sections,
    }
    return render(request, 'batch_sections.html', context)

@login_required 
def add_time_section(request, center_id, batch_id):
    if request.method == 'POST':
        center = Center.objects.get(pk=center_id)
        batch = Batch.objects.get(pk=batch_id)
        name = request.POST.get('name')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        section = TimeSection.objects.create(
            name=name,
            start_time=start_time,
            end_time=end_time,
            batch=batch,
        )
        return redirect('batch_sections', center_id=center.id, batch_id=batch.id)
    else:
        center = Center.objects.get(pk=center_id)
        batch = Batch.objects.get(pk=batch_id)
        context = {
            'center': center,
            'batch':batch
        }
        return render(request, 'add_time_section.html', context)
    
# Edit Time section #
@login_required 
def update_time_section(request, center_id, batch_id, section_id):
    center = Center.objects.get(pk=center_id)
    batch = Batch.objects.get(pk=batch_id)
    section = get_object_or_404(TimeSection, pk=section_id)
    if request.method == 'POST':
        section.name = request.POST.get('name')
        section.start_time = request.POST.get('start_time')
        section.end_time = request.POST.get('end_time')
        section.save()
        return redirect('batch_sections', center_id=center.id, batch_id=batch.id)

    context = {'section': section}
    return render(request, 'update_time_section.html', context)

@login_required 
def delete_section(request, center_id , batch_id, section_id):
    center = get_object_or_404(Center, pk = center_id)
    batch =get_object_or_404(Batch, pk=batch_id)
    section = get_object_or_404(TimeSection, pk=section_id)
    
    section.delete()
    return redirect('batch_sections', center_id=center.id, batch_id=batch.id, )

# Attendance Date list #
# def attendance_date(request, center_id, batch_id, section_id):
#     center = Center.objects.get(pk=center_id)
#     batch = Batch.objects.get(pk=batch_id)
#     section = TimeSection.objects.get(pk=section_id)
#     date_list = Attendance.objects.filter(time_section=section).values('date').distinct()

#     if request.method == 'POST':
#         selected_date = request.POST.get('date')
#         return redirect('attendance_detail', center_id=center_id, batch_id=batch.id, section_id=section_id, date=selected_date)

#     context = {
#         'center': center,
#         'section': section,
#         'batch':batch,
#         'date_list': date_list,
#     }

#     return render(request, 'attendance_date.html', context)

@login_required 
def attendance_date(request, center_id, batch_id, section_id):
    center = Center.objects.get(pk=center_id)
    batch = Batch.objects.get(pk=batch_id)
    section = TimeSection.objects.get(pk=section_id)
    date_list = Attendance.objects.filter(time_section=section).values('date').distinct()

    context = {
        'center': center,
        'section': section,
        'batch':batch,
        'date_list': date_list,
    }

    return render(request, 'attendance_date.html', context)

@login_required 
def delete_attendance_date(request, center_id, batch_id, section_id, date):
    center = Center.objects.get(pk=center_id)
    batch = Batch.objects.get(pk=batch_id)
    section = TimeSection.objects.get(pk=section_id)
    attendance_list = Attendance.objects.filter(time_section=section, date=date)
    attendance_list.delete()

    return redirect('attendance_date', center_id=center_id, batch_id=batch_id, section_id=section_id)


@login_required 
def add_attendance(request, center_id, batch_id, section_id):
    center = Center.objects.get(pk=center_id)
    batch = Batch.objects.get(pk=batch_id)
    section = TimeSection.objects.get(pk=section_id)
    students = Student.objects.filter(batch=section.batch)

    if request.method == 'POST':
        students_selected = request.POST.getlist('student')
        date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()

        # Check if attendance already exists for this batch and date
        if Attendance.objects.filter(date=date, time_section__batch=batch).exists():
            messages.warning(request, f"Attendance for {date} has already been taken for this batch.")
        else:
            # Loop through all students and create attendance records
            for student in students:
                if str(student.id) in students_selected:
                    data = Attendance(date=date, time_section=section, Student=student, Attandance='Precent')
                    data.save()
                else:
                    data = Attendance(date=date, time_section=section, Student=student, Attandance='Absent')
                    data.save()

            # Mark time section as ended
            section.Ended = True
            section.save()

            messages.success(request, f"Attendance for {date} has been taken for this batch.")

            return redirect('attendance_date', center_id=center.id, batch_id=batch.id, section_id=section.id)

    context = {
        'center': center,
        'section': section,
        'students': students,
        'batch': batch,
    }
    return render(request, 'add_attendance.html', context)


# @login_required     
# def edit_attendance(request, center_id, section_id, attendance_id):
#     center = Center.objects.get(pk=center_id)
#     section = TimeSection.objects.get(pk=section_id)
#     attendance = Attendance.objects.get(pk=attendance_id)

#     if request.method == 'POST':
#         students_selected = request.POST.getlist('student')
#         date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()

#         attendance.date = date
#         attendance.student.clear()
#         for student_id in students_selected:
#             student = Student.objects.get(pk=student_id)
#             attendance.student.add(student)

#         attendance.save()
#         return redirect('attendance_detail', center_id=center.id, section_id=section.id, attendance_id=attendance.id)

#     else:
#         students = Student.objects.filter(center=center)
#         context = {
#             'center': center,
#             'section': section,
#             'students': students,
#             'attendance': attendance
#         }

#         return render(request, 'edit_attendance.html', context)


@login_required 
def attendance_detail(request, center_id, batch_id, section_id, date):
    center = Center.objects.get(pk=center_id)
    batch = Batch.objects.get(pk=batch_id)
    section = TimeSection.objects.get(pk=section_id)
    date_obj = datetime.strptime(date, '%Y-%m-%d').date().strftime('%Y-%m-%d')

    attendance_list = Attendance.objects.filter(time_section=section, date=date_obj)

    context = {
        'center': center,
        'batch':batch,
        'section': section,
        'date': date,
        'attendance_list': attendance_list,
    }

    return render(request, 'attendance_detail.html', context)

# --------------------------------------------- Coach ------------------------------------------------------ #

@login_required
def add_coach(request):
    centers = Center.objects.all()
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
        )
        coach = Coach.objects.create(
            user=user,
            primary_mobile=request.POST.get('primary_mobile'),
            secondary_mobile=request.POST.get('secondary_mobile'),
            place=request.POST.get('place'),
            years_of_experience=request.POST.get('years_of_experience'),
            center_id=request.POST.get('center_id'),
        )
        return redirect('coach_detail', pk=coach.pk)
    context = {
        'centers': centers,
    }
    return render(request, 'add_coach.html', context)

@login_required
def delete_coach(request, pk):
    coach = get_object_or_404(Coach, pk=pk)
    coach.delete()
    return redirect('coach_list')

@login_required
def coach_detail(request, pk):
    coach = get_object_or_404(Coach, pk=pk)
    return render(request, 'coach_detail.html', {'coach': coach})

@login_required
def coach_list(request):
    coaches = Coach.objects.all()
    return render(request, 'coach_list.html', {'coaches': coaches})

# --------------------------------- Batches ---------------------------------------------------------- #

@login_required
def batch_list(request):
    batches = Batch.objects.all()
    return render(request, 'batch_list.html', {'batches': batches})

@login_required
def batch_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        center_id = request.POST['center']
        batch = Batch(name=name, center_id=center_id)
        batch.save()
        return redirect('batch-list')
    else:
        centers = Center.objects.all()
        return render(request, 'batch_create.html', {'centers': centers})

@login_required
def batch_delete(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        batch.delete()
        return redirect('batch-list')
    return render(request, 'batch_confirm_delete.html', {'batch': batch})

# --------------------------------- Transfor -------------------------------------------------------- #

@login_required
def trasnfor_center(request):
    center = Center.objects.all()
    return render (request, 'transfor_center.html', {'center':center})

@login_required
def transfor_student(request, center_id):
    center = Center.objects.get(pk=center_id)
    student = Student.objects.filter(center=center)
    context = {
        'center' : center,
        'student' : student
    }
    return render (request, 'transfor_student.html', context)

@login_required
def transfor(request, center_id, student_id):
    center = Center.objects.get(pk=center_id)
    student = Student.objects.get(pk=student_id)
    centers = Center.objects.all()
    batches = Batch.objects.filter(center=center)
    if request.method == 'POST':
        student.center_id = request.POST.get('center')
        student.batch_id = request.POST.get('batch')
        student.save()
        return redirect('transfor_center')

    context = {
        'center': center,
        'centers': centers,
        'student': student,
        'batches': batches,
    }
    return render(request, 'transfor.html', context)

@login_required
def get_batches(request, center_id):
    batches = list(Batch.objects.filter(center_id=center_id).values('pk', 'name'))
    return JsonResponse({'batches': batches})




