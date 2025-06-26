from django.contrib import admin
from .models import Student, Teacher, Room, Course, CourseRegistration, Attendance, Marks

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'date_of_birth', 'date_joined', 'emergency_phone']
    list_filter = ['date_joined', 'date_of_birth']
    search_fields = ['student_id', 'full_name', 'emergency_phone']
    ordering = ['student_id']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_id', 'full_name', 'subject', 'date_joined']
    list_filter = ['subject', 'date_joined']
    search_fields = ['teacher_id', 'full_name', 'subject']
    ordering = ['teacher_id']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'capacity']
    search_fields = ['room_number']
    ordering = ['room_number']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'teacher', 'room']
    list_filter = ['teacher', 'room']
    search_fields = ['course_name', 'teacher__full_name']
    ordering = ['course_name']

@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'registration_date']
    list_filter = ['course', 'registration_date']
    search_fields = ['student__full_name', 'course__course_name']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'date', 'status']
    list_filter = ['status', 'date', 'course']
    search_fields = ['student__full_name', 'course__course_name']
    ordering = ['-date']

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'subject', 'marks', 'total_marks', 'get_percentage', 'get_grade', 'date_recorded']
    list_filter = ['course', 'subject', 'date_recorded']
    search_fields = ['student__full_name', 'course__course_name', 'subject']
    ordering = ['-date_recorded']
