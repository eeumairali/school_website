#!/usr/bin/env python
"""
Script to set admin password
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from django.contrib.auth.models import User

# Set admin password
try:
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('admin123')
    admin_user.save()
    print("Admin password set to: admin123")
    print("Username: admin")
    print("Password: admin123")
except User.DoesNotExist:
    print("Admin user not found!")
