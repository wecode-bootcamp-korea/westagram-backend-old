import json
from django.views import View 
from .models import Users
from django.http import JsonResponse
from .models import Post_register
from user.views import login_decorator
class Post(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        image_url = data['image_url']
        user = Users.objects.get(email = data['user'])
        Post_register.objects.create(user = user, image_url = image_url)
        return JsonResponse({'message' : 'SUCCESS'}, status=200)
            
        
