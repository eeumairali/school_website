from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from students.models import Student, Teacher, Room, Course, CourseRegistration, Marks
import datetime

class Command(BaseCommand):
    help = 'Setup initial demo data for the school management system'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up demo data...'))
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@school.com',
                password='admin123',
                first_name='System',
                last_name='Administrator'
            )
            UserProfile.objects.create(user=admin_user, user_type='admin')
            self.stdout.write(self.style.SUCCESS('Admin user created: admin/admin123'))
        
        # Create demo teacher
        if not User.objects.filter(username='teacher1').exists():
            teacher_user = User.objects.create_user(
                username='teacher1',
                email='teacher1@school.com',
                password='teacher123',
                first_name='John',
                last_name='Smith'
            )
            UserProfile.objects.create(user=teacher_user, user_type='teacher')
            Teacher.objects.create(
                user=teacher_user,
                teacher_id='T001',
                full_name='John Smith',
                subject='Mathematics',
                date_joined=datetime.date.today()
            )
            self.stdout.write(self.style.SUCCESS('Teacher created: teacher1/teacher123'))
        
        # Create demo students
        students_data = [
            ('student1', 'Alice Johnson', 'S001', '2000-05-15'),
            ('student2', 'Bob Williams', 'S002', '2001-03-22'),
            ('student3', 'Carol Davis', 'S003', '2000-08-10'),
        ]
        
        for username, full_name, student_id, dob in students_data:
            if not User.objects.filter(username=username).exists():
                student_user = User.objects.create_user(
                    username=username,
                    email=f'{username}@school.com',
                    password='student123',
                    first_name=full_name.split()[0],
                    last_name=full_name.split()[1]
                )
                UserProfile.objects.create(user=student_user, user_type='student')
                Student.objects.create(
                    user=student_user,
                    student_id=student_id,
                    full_name=full_name,
                    date_of_birth=datetime.datetime.strptime(dob, '%Y-%m-%d').date(),
                    date_joined=datetime.date.today(),
                    emergency_phone='+1234567890'
                )
                self.stdout.write(self.style.SUCCESS(f'Student created: {username}/student123'))
        
        # Create demo rooms
        if not Room.objects.exists():
            rooms_data = [
                ('A101', 30),
                ('A102', 25),
                ('B201', 35),
            ]
            
            for room_number, capacity in rooms_data:
                Room.objects.create(room_number=room_number, capacity=capacity)
            
            self.stdout.write(self.style.SUCCESS('Rooms created'))
        
        # Create demo courses
        if not Course.objects.exists():
            teacher = Teacher.objects.first()
            room = Room.objects.first()
            
            if teacher and room:
                courses_data = [
                    'Mathematics 101',
                    'Algebra Basics',
                    'Geometry Fundamentals',
                ]
                
                for course_name in courses_data:
                    Course.objects.create(
                        course_name=course_name,
                        teacher=teacher,
                        room=room
                    )
                
                self.stdout.write(self.style.SUCCESS('Courses created'))
        
        # Create demo marks
        if not Marks.objects.exists():
            students = Student.objects.all()
            courses = Course.objects.all()
            
            if students and courses:
                subjects = ['Mathematics', 'Algebra', 'Geometry']
                
                for student in students:
                    for course in courses:
                        for subject in subjects:
                            # Create random marks for demo
                            import random
                            marks = random.randint(60, 95)
                            total_marks = 100
                            
                            Marks.objects.create(
                                student=student,
                                course=course,
                                subject=subject,
                                marks=marks,
                                total_marks=total_marks,
                            )
                
                self.stdout.write(self.style.SUCCESS('Demo marks created'))
        
        self.stdout.write(self.style.SUCCESS('Demo data setup completed!'))
        self.stdout.write(self.style.WARNING('Login credentials:'))
        self.stdout.write(self.style.WARNING('Admin: admin/admin123'))
        self.stdout.write(self.style.WARNING('Teacher: teacher1/teacher123'))
        self.stdout.write(self.style.WARNING('Students: student1/student123, student2/student123, student3/student123'))
