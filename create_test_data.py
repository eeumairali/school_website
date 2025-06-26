#!/usr/bin/env python
"""
Create test users for the school management system
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from students.models import Student, Teacher, Room
from datetime import date

def create_test_data():
    print("Creating test data...")
    
    # Create admin user profile if admin exists but no profile
    try:
        admin_user = User.objects.get(username='admin')
        if not hasattr(admin_user, 'userprofile'):
            UserProfile.objects.create(user=admin_user, user_type='admin')
            print("✅ Admin profile created")
        else:
            print("✅ Admin profile already exists")
    except User.DoesNotExist:
        print("❌ Admin user not found")
    
    # Create a test student
    if not User.objects.filter(username='student1').exists():
        student_user = User.objects.create_user(
            username='student1',
            password='student123',
            email='student1@school.com',
            first_name='John',
            last_name='Doe'
        )
        
        # Create user profile
        UserProfile.objects.create(user=student_user, user_type='student')
        
        # Create student record
        Student.objects.create(
            user=student_user,
            student_id='STU001',
            full_name='John Doe',
            date_of_birth=date(2005, 6, 15),
            date_joined=date.today(),
            emergency_phone='+1234567890'
        )
        print("✅ Test student created - Username: student1, Password: student123")
    else:
        print("✅ Test student already exists")
    
    # Create a test teacher
    if not User.objects.filter(username='teacher1').exists():
        teacher_user = User.objects.create_user(
            username='teacher1',
            password='teacher123',
            email='teacher1@school.com',
            first_name='Jane',
            last_name='Smith'
        )
        
        # Create user profile
        UserProfile.objects.create(user=teacher_user, user_type='teacher')
        
        # Create teacher record
        Teacher.objects.create(
            user=teacher_user,
            teacher_id='TEA001',
            full_name='Jane Smith',
            subject='Mathematics',
            date_joined=date.today()
        )
        print("✅ Test teacher created - Username: teacher1, Password: teacher123")
    else:
        print("✅ Test teacher already exists")
    
    # Create some rooms if they don't exist
    if not Room.objects.exists():
        Room.objects.create(room_number='101', capacity=30)
        Room.objects.create(room_number='102', capacity=25)
        Room.objects.create(room_number='201', capacity=35)
        print("✅ Test rooms created")
    else:
        print("✅ Rooms already exist")
    
    print("\n🎉 Test data creation completed!")
    print("\n📝 Login credentials:")
    print("Admin: username=admin, password=admin123")
    print("Student: username=student1, password=student123")
    print("Teacher: username=teacher1, password=teacher123")

if __name__ == "__main__":
    create_test_data()
