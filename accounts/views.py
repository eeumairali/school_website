from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from students.models import Student, Teacher
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user = self.request.user
        try:
            profile = UserProfile.objects.get(user=user)
            if profile.user_type == 'admin':
                return reverse_lazy('admin_dashboard')
            elif profile.user_type == 'student':
                return reverse_lazy('student_dashboard')
            elif profile.user_type == 'teacher':
                return reverse_lazy('teacher_dashboard')
        except UserProfile.DoesNotExist:
            pass
        return reverse_lazy('home')

@login_required
def dashboard(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.user_type == 'admin':
            return redirect('admin_dashboard')
        elif profile.user_type == 'student':
            return redirect('student_dashboard')
        elif profile.user_type == 'teacher':
            return redirect('teacher_dashboard')
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found. Please contact administrator.')
    
    return render(request, 'accounts/dashboard.html')

@login_required
def admin_dashboard(request):
    if not (request.user.is_superuser or 
            (hasattr(request.user, 'userprofile') and request.user.userprofile.user_type == 'admin')):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    recent_students = Student.objects.order_by('-date_joined')[:5]
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'recent_students': recent_students,
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        from students.models import CourseRegistration, Marks
        
        courses = CourseRegistration.objects.filter(student=student)
        marks = Marks.objects.filter(student=student).order_by('-date_recorded')[:5]
        
        context = {
            'student': student,
            'courses': courses,
            'recent_marks': marks,
        }
        return render(request, 'accounts/student_dashboard.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('dashboard')

@login_required
def teacher_dashboard(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        from students.models import Course
        
        courses = Course.objects.filter(teacher=teacher)
        
        context = {
            'teacher': teacher,
            'courses': courses,
        }
        return render(request, 'accounts/teacher_dashboard.html', context)
    except Teacher.DoesNotExist:
        messages.error(request, 'Teacher profile not found.')
        return redirect('dashboard')
