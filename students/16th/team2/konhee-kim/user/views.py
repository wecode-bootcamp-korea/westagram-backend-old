import json
import re

from django.http  import JsonResponse
from django.views import View

from user.models  import User


class SignUpView(View):

    def post(self, request):
        data = json.loads(request.body)
        
        email, mobile_number = check_email_or_mobile(data['email_or_mobile'])
        if bool(email) and bool(mobile_number) == False:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
        
        if not(validate_password(data['password'])):
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

        # existence check
        if email and User.objects.filter(email = email).exists():
            return JsonResponse({'MESSAGE': 'EXISTENCE_ERROR'}, status=400)
        if mobile_number and User.objects.filter(mobile_number = mobile_number).exists():
            return JsonResponse({'MESSAGE': 'EXISTENCE_ERROR'}, status=400)

        a_user = User.objects.create(
            email         = email
            mobile_number = mobile_number
            full_name     = data['full_name']
            username      = data['username']
            password      = data['password']
        )

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
       

def check_email_or_mobile(item):

    if validate_mobile(item): # validate_mobile is more strict than validate_email
        email = ''
        mobile_number = int(''.join(item.split('-')))
        return email, mobile_number

    if validate_email(item):
        email = item
        mobile_number = None
        return email, mobile_number
        
    email, mobile_number = ('', None)
    return email, mobile_number

def validate_email(email):
    """
    for email validation. check email_addresss whether include '@' & '.'
    """
    try:
        return re.match(r".+@.+\..+", email).group(0) == email:
    except:
        return False:
    
def validate_mobile(mobile):
    """
    for mobile_number validation. 
    """
    try:
        return re.match(
                r"^01[0-9]-?[0-9][0-9][0-9][0-9]-?[0-9][0-9][0-9][0-9]$", mobile
                ).group(0) == mobile
    except:
        return False:

def validate_password(password):
    """
    for password validation. check password > 8 characters
    """
    return re.match(r".*", password).span()[1] >= 8  
