import json
import re

from django.http  import JsonResponse
from django.views import View

from user.models  import User


class SignUpView(View):

    def post(self, request):
        data          = json.loads(request.body)
        email, mobile = check_email_or_mobile(data['email_or_mobile'])
        username      = data['username']

        if not (email or mobile): # unexpected value input
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
        
        if not(validate_password(data['password'])):
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

        if not username:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

        # existence check
        if email    and User.objects.filter(email         = email).exists():
            return JsonResponse({'MESSAGE': 'EXISTENCE_ERROR'}, status=400)
       
        if mobile   and User.objects.filter(mobile_number = mobile).exists():
            return JsonResponse({'MESSAGE': 'EXISTENCE_ERROR'}, status=400)
        
        if username and User.objects.filter(username      = username).exists():
            return JsonResponse({'MESSAGE': 'EXISTENCE_ERROR'}, status=400)

        # create user account
        a_user = User.objects.create(
            email         = email,
            mobile_number = mobile,
            full_name     = data['full_name'],
            username      = username,
            password      = data['password']
        )

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

class LogInView(View):

    def post(self, request):
        data          = json.loads(request.body)
        email, mobile = check_email_or_mobile(data['phone_name_email'])
        password      = data['password']

        if not password:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

        if email:
            try:
                if User.objects.get(email=email).password == password:
                    return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)
            except:
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)


        if mobile:
            try:
                if User.objects.get(mobile_number=mobile).password == password:
                    return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)
            except:
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)
        
        username = data['phone_name_email']

        if username:
            try:
                if User.objects.get(username=username).password == password:
                    return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)
            except:
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)
        
        # empty input.
        return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

def check_email_or_mobile(item):

    if validate_mobile(item):
        email = ''
        mobile_number = ''.join(item.split('-'))
        return email, mobile_number

    if validate_email(item):
        email = item
        mobile_number = ''
        return email, mobile_number
        
    email, mobile_number = ('', '')
    return email, mobile_number

def validate_email(email):
    """
    for email validation. check email_addresss whether include '@' & '.'
    """
    try:
        return re.match(r".+@.+\..+", email).group(0) == email
    except:
        return False
    
def validate_mobile(mobile):
    """
    for mobile_number validation. 
    """
    try:
        return re.match(
                r"^01[0-9]-?[0-9][0-9][0-9][0-9]-?[0-9][0-9][0-9][0-9]$", mobile
                ).group(0) == mobile
    except:
        return False

def validate_password(password):
    """
    for password validation. check password > 8 characters
    """
    return re.match(r".*", password).span()[1] >= 8  
