# Django School Management System

A complete school management system built with Django and SQLite3.

## Features

- **Admin Dashboard**: Manage students, teachers, courses, and marks
- **Student Portal**: Students can view their marks and attendance
- **Teacher Portal**: Teachers can manage their courses
- **User Authentication**: Separate login for admin, students, and teachers

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
```
Or use the existing admin user:
- Username: `admin`
- Password: `admin123`

### 4. Start Development Server
```bash
python manage.py runserver
```

### 5. Access the Application
- Admin Panel: http://127.0.0.1:8000/admin/
- Main Application: http://127.0.0.1:8000/

## Models

- **Student**: Student information and user account
- **Teacher**: Teacher information and user account  
- **Room**: Classroom information
- **Course**: Course details with teacher and room assignment
- **CourseRegistration**: Student enrollment in courses
- **Attendance**: Student attendance records
- **Marks**: Student grades and marks

## Admin Features

- Add/Edit/Delete students, teachers, rooms, and courses
- Manage student enrollments
- Record attendance
- Enter and manage student marks
- View comprehensive reports

## Student Features

- View personal information
- Check course enrollments
- View marks and grades
- Check attendance records

## File Structure

```
django_based_school/
├── manage.py
├── requirements.txt
├── db.sqlite3                 # SQLite database
├── school_management/         # Main project settings
├── accounts/                  # User authentication app
├── students/                  # Student management app
├── templates/                 # HTML templates
├── static/                    # CSS, JS, images
└── README.md
```

## Database

The application uses SQLite3 database (`db.sqlite3`) which is perfect for development and small deployments. The database file is created automatically when you run migrations.

## Deployment

This application is ready for deployment on platforms like:
- Heroku
- PythonAnywhere
- DigitalOcean
- AWS

The SQLite3 database makes it easy to deploy without setting up external database servers.
