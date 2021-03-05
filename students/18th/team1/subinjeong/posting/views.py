import json

from django.http  import JsonResponse
from django.views import View

from .models import *


class UploadView(View):

    def post(self,request):   
        login_data = json.loads(request.body)

        try:
            

        except
            # key error
            return JsonResponse({'message': 'INVALID_USER'}, status = 401)