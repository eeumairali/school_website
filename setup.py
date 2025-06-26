#!/usr/bin/env python
"""
Django School Management System Setup Script
This script sets up the SQLite3 database and creates initial data.
"""

import os
import sys
import subprocess

def run_command(command):
    """Run a command and print its output"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def setup_django():
    """Setup Django project with SQLite3"""
    print("Setting up Django School Management System with SQLite3...")
    
    # Make migrations
    print("\n1. Creating migrations...")
    if not run_command("python manage.py makemigrations"):
        return False
    
    # Apply migrations
    print("\n2. Applying migrations...")
    if not run_command("python manage.py migrate"):
        return False
    
    # Create superuser
    print("\n3. Creating superuser...")
    print("You will be prompted to create an admin user...")
    run_command("python manage.py createsuperuser")
    
    # Collect static files
    print("\n4. Collecting static files...")
    run_command("python manage.py collectstatic --noinput")
    
    print("\n✅ Setup completed successfully!")
    print("\nTo start the development server, run:")
    print("python manage.py runserver")
    print("\nThen visit: http://127.0.0.1:8000/admin/")
    
    return True

if __name__ == "__main__":
    setup_django()
