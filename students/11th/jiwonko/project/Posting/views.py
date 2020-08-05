import json

from django.views import View
from django.http  import JsonResponse

from .models     import Post
from User.models import User

class PostView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(id = data['user_id']).exists():
                user = User.objects.get(id = data['user_id'])
                Post(
                    user    = user,
                    content = data['content'],
                    img_url = data['img_url']
                ).save()
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)
            else:
                return JsonResponse({'message' : 'NO_EXISTS_USER'}, status = 401)
        except Exception as e:
                return JsonResponse({'message' : f'{e}'}, status = 401)










