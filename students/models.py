from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_joined = models.DateField()
    emergency_phone = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.student_id} - {self.full_name}"
    
    class Meta:
        ordering = ['student_id']

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)
    date_joined = models.DateField()
    
    def __str__(self):
        return f"{self.teacher_id} - {self.full_name}"
    
    class Meta:
        ordering = ['teacher_id']

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    
    def __str__(self):
        return f"Room {self.room_number} (Capacity: {self.capacity})"
    
    class Meta:
        ordering = ['room_number']

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, through='CourseRegistration')
    
    def __str__(self):
        return self.course_name
    
    class Meta:
        ordering = ['course_name']

class CourseRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"{self.student} - {self.course}"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    class Meta:
        unique_together = ['student', 'course', 'date']
    
    def __str__(self):
        return f"{self.student} - {self.course} - {self.date} - {self.status}"

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    marks = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    date_recorded = models.DateField(auto_now_add=True)
    
    def get_percentage(self):
        if self.total_marks > 0:
            return round((self.marks / self.total_marks) * 100, 2)
        return 0
    
    def get_grade(self):
        percentage = self.get_percentage()
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B'
        elif percentage >= 60:
            return 'C'
        elif percentage >= 50:
            return 'D'
        else:
            return 'F'
    
    class Meta:
        verbose_name_plural = "Marks"
        unique_together = ['student', 'course', 'subject']
    
    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks}/{self.total_marks}"
