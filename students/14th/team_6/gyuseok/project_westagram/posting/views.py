import json
from django.views import View
from django.http  import JsonResponse
from .models import Post
from user.models import User
from django.db.models import Q

# Create your views here.
class RegisterView(View):
    def post(self, request):

        NECESSERY_KEYS = ('username', 'content', 'image_url')
        data = json.loads(request.body)

        for k in NECESSERY_KEYS:
            if k not in data.keys():
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)


        if User.objects.filter(name=data['username']).exists():
            key = User.objects.get(name=data['username'])
            Post.objects.create( content = data['content'],
                                 image   = data['image_url'],
                                 user    = key
                               )
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        else:
            return JsonResponse({'message': 'NOT EXIST USER'}, status=400)


class ExpressView(View):
    def get(self, request):
        return JsonResponse({'data' : list(Post.objects.values())}, status=200)

