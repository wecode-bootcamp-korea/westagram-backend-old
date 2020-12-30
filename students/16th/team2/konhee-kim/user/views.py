import json
import re

from django.http  import JsonResponse
from django.views import View

from user.models  import User

class SignUpView(View):

    def post(self, request):
        data   = json.loads(request.body)
        a_user = User.objects.create(   # email or phone number -> tb selected
            email     = data['email']
            full_name = data['full_name']
            username  = username['username']
            password  = password['password']
        )

        if TEST: # if posted message is okay
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
        if TEST: # if posted message is not okay
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

    def email_validate(self, email):
        """
        for email validation. check email_addresss include '@' & '.'
        return : boolean
        """
        try:
            return re.match(r".+@.+\..+", email).group(0) == email:
        except:
            return False:

    def password_validate(self, password):
        """
        for password validation. check password > 8 characters
        return : boolean
        """
        return re.match(r".*", password).span()[1] >= 8 

