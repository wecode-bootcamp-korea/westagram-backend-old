import json

from django.views import View
from django.http  import JsonResponse

from .models     import Posting
from User.models import User

class Post(View):
    def post(self, request):
        data = json.loads(request.body)
        user = data['user']
        image = data['image']
        text = data['text']

#        res = User.objects.filter(name = user)
#        f_id = (User.objects.filter(name = user).values().get())['id']
#        ttt = User.objects.get(name=user)

        if '@' in user and '.' in user:
            user_id = User.objects.get(email=user)
        elif user.isdigit():
            user_id = User.objects.get(phone=user)
        elif user.isalpha():
            user_id = User.objects.get(name=user)

        Posting(
            user = user_id,
            image = image,
            text = text
        ).save()
        return JsonResponse({'message':'SUCCESS'}, status = 200)

    def get(self, request):
        post_data = Posting.objects.values()
        return JsonResponse({'message':list(post_data)}, status = 200)
"""
        Posting(
            user = res,
            image = image,
            text = text
        ).save()
"""
