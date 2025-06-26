from django import template
from accounts.models import UserProfile

register = template.Library()

@register.filter
def user_type(user):
    """Get user type safely"""
    try:
        return user.userprofile.user_type
    except (AttributeError, UserProfile.DoesNotExist):
        return None

@register.filter
def is_admin(user):
    """Check if user is admin"""
    if user.is_superuser:
        return True
    try:
        return user.userprofile.user_type == 'admin'
    except (AttributeError, UserProfile.DoesNotExist):
        return False

@register.filter
def is_student(user):
    """Check if user is student"""
    try:
        return user.userprofile.user_type == 'student'
    except (AttributeError, UserProfile.DoesNotExist):
        return False

@register.filter
def is_teacher(user):
    """Check if user is teacher"""
    try:
        return user.userprofile.user_type == 'teacher'
    except (AttributeError, UserProfile.DoesNotExist):
        return False
