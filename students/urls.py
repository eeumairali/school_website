from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.add_student, name='add_student'),
    path('marks/', views.student_marks, name='student_marks'),
    path('add-marks/', views.add_marks, name='add_marks'),
    path('marks-list/', views.marks_list, name='marks_list'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('attendance/', views.student_attendance, name='student_attendance'),
]
