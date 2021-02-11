import re

from django.core.exceptions import ValidationError

from .models import User

def name_overlap(post_data):
    if User.objects.filter(name = post_data) and post_data != "":
        raise ValidationError("Name is Overlapped.")

def email_overlap(post_data):
    if User.objects.filter(email = post_data):
        raise ValidationError("Email is Overlapped")

def phone_number_overlap(post_data):
    if User.objects.filter(phone_number = post_data) and post_data != "":
        raise ValidationError("Phone_number is Overlapped")

def email_validate(post_data):
    if not re.search('.+[@].+[.].+', post_data):
        raise ValidationError("Email is Wrong")

def password_validate(post_data):
    if not re.search('.{8,}', post_data):
        raise ValidationError("Password is Wrong.")
