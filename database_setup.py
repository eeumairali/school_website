"""
Simple database setup script for Django SQLite3 database.
This script is not needed for SQLite3 as Django handles everything automatically.
Just run: python manage.py migrate
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

def create_sample_data():
    """Create some sample data for testing"""
    from django.contrib.auth.models import User
    from students.models import Student, Teacher, Room, Course
    from accounts.models import UserProfile
    from datetime import date
    
    print("Creating sample data...")
    
    # Create admin user if doesn't exist
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@school.com',
            password='admin123'
        )
        UserProfile.objects.create(user=admin_user, user_type='admin')
        print("Admin user created: username=admin, password=admin123")
    
    # Create sample rooms
    if not Room.objects.exists():
        Room.objects.create(room_number='101', capacity=30)
        Room.objects.create(room_number='102', capacity=25)
        Room.objects.create(room_number='201', capacity=35)
        print("Sample rooms created")
    
    print("Sample data creation completed!")

if __name__ == "__main__":
    create_sample_data()
