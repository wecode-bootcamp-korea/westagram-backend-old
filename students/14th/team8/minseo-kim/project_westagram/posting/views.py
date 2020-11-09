import json
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Post
from user.models import User

class PostView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            
            if not User.objects.filter(id=data['user_id']).exists():
                return JsonResponse({'message':'INVALID_USER'},status=401)
            
            Post.objects.create(
                image_url=data['image_url'],
                user_id=data['user_id']
            )

            return JsonResponse({'message':'SUCCESS'},status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)



