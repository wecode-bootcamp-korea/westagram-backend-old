import json

from django.http import JsonResponse
from django.views import View
from django.utils import timezone

from user.models import User
from posting.models import Board

# Create your views here.


class Posting(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user_info = data['username']
            image_url = data['image_url']
            # get datas from body of request
            # user_info related with User model  of foreignKey from user.models.py
#            user_id =  User.objects.get(username = data['username']).id
#            Board.objects.create(user=user_id, image_url=image_url)

            u1 = User.objects.get(id=1)




            Board.objects.create(username=user_info, image_url=image_url)

            return JsonResponse({u1 : 'SUCCESS'})
        except:
            return JsonResponse({u1 : 'ERROR'})

