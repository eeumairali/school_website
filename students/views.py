from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Student, Teacher, Course, Marks, Attendance, Room, CourseRegistration
from accounts.models import UserProfile
import datetime

@login_required
def student_list(request):
    # Check if user is admin
    if not (request.user.is_superuser or 
            (hasattr(request.user, 'userprofile') and request.user.userprofile.user_type == 'admin')):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    students = Student.objects.all().order_by('student_id')
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'students/student_list.html', {'page_obj': page_obj})

@login_required
def add_student(request):
    # Check if user is admin
    if not (request.user.is_superuser or 
            (hasattr(request.user, 'userprofile') and request.user.userprofile.user_type == 'admin')):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        student_id = request.POST.get('student_id')
        full_name = request.POST.get('full_name')
        date_of_birth = request.POST.get('date_of_birth')
        emergency_phone = request.POST.get('emergency_phone')
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=full_name.split()[0] if full_name else '',
                last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
            )
            
            # Create user profile
            UserProfile.objects.create(user=user, user_type='student')
            
            # Create student
            Student.objects.create(
                user=user,
                student_id=student_id,
                full_name=full_name,
                date_of_birth=date_of_birth,
                date_joined=datetime.date.today(),
                emergency_phone=emergency_phone
            )
            
            messages.success(request, f'Student {full_name} added successfully!')
            return redirect('student_list')
            
        except Exception as e:
            messages.error(request, f'Error adding student: {str(e)}')
    
    return render(request, 'students/add_student.html')

@login_required
def student_marks(request):
    try:
        student = Student.objects.get(user=request.user)
        marks = Marks.objects.filter(student=student).order_by('-date_recorded')
        
        context = {
            'student': student,
            'marks': marks,
        }
        return render(request, 'students/student_marks.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('dashboard')

@login_required
def add_marks(request):
    # Check if user is admin or teacher
    if not (request.user.is_superuser or 
            (hasattr(request.user, 'userprofile') and 
             request.user.userprofile.user_type in ['admin', 'teacher'])):
        messages.error(request, 'Access denied. Admin or Teacher privileges required.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')
        subject = request.POST.get('subject')
        marks = request.POST.get('marks')
        total_marks = request.POST.get('total_marks')
        
        try:
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
            
            mark_obj, created = Marks.objects.update_or_create(
                student=student,
                course=course,
                subject=subject,
                defaults={
                    'marks': marks,
                    'total_marks': total_marks,
                }
            )
            
            action = 'added' if created else 'updated'
            messages.success(request, f'Marks {action} successfully for {student.full_name}!')
            return redirect('marks_list')
            
        except Exception as e:
            messages.error(request, f'Error adding marks: {str(e)}')
    
    students = Student.objects.all()
    courses = Course.objects.all()
    
    context = {
        'students': students,
        'courses': courses,
    }
    return render(request, 'students/add_marks.html', context)

@login_required
def marks_list(request):
    # Check if user is admin or teacher
    if not (request.user.is_superuser or 
            (hasattr(request.user, 'userprofile') and 
             request.user.userprofile.user_type in ['admin', 'teacher'])):
        messages.error(request, 'Access denied. Admin or Teacher privileges required.')
        return redirect('dashboard')
    
    marks = Marks.objects.all().order_by('-date_recorded')
    paginator = Paginator(marks, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'students/marks_list.html', {'page_obj': page_obj})

@login_required
def course_list(request):
    courses = Course.objects.all().order_by('course_name')
    teachers = Teacher.objects.all()
    rooms = Room.objects.all()
    
    context = {
        'courses': courses,
        'teachers': teachers,
        'rooms': rooms,
    }
    return render(request, 'students/course_list.html', context)

@login_required
def add_course(request):
    # Check if user is admin
    if not (request.user.is_superuser or 
            (hasattr(request.user, 'userprofile') and request.user.userprofile.user_type == 'admin')):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        teacher_id = request.POST.get('teacher_id')
        room_id = request.POST.get('room_id')
        
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            room = Room.objects.get(id=room_id)
            
            Course.objects.create(
                course_name=course_name,
                teacher=teacher,
                room=room
            )
            
            messages.success(request, f'Course "{course_name}" added successfully!')
            
        except Exception as e:
            messages.error(request, f'Error adding course: {str(e)}')
    
    return redirect('course_list')

@login_required
def student_attendance(request):
    try:
        student = Student.objects.get(user=request.user)
        attendance = Attendance.objects.filter(student=student).order_by('-date')
        
        context = {
            'student': student,
            'attendance': attendance,
        }
        return render(request, 'students/student_attendance.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('dashboard')
