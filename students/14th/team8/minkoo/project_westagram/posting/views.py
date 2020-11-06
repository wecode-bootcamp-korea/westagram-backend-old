import json
import re

from django.views import View
from django.http import JsonResponse

from user.models import User
from .models import Post

class PostsView(View):
    def post(self, request):
        data = json.loads(request.body)
        url_check = re.compile('https?://[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+/[a-zA-Z0-9-_.=?/]*')

        if 'image_url' not in data or 'user_id' not in data or 'content' not in data  or len(data) != 3:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        if not re.match(url_check, data['image_url']):
            return JsonResponse({'message':'INVALID_IMAGE_URL'}, status=400)

        try:
            user_model = User.objects.get(id=data['user_id'])
            Post.objects.create(
                user_id = user_model.id,
                content = data['content'],
                image_url = data['image_url']
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except User.DoseNotExist:
            return JsonResponse({'message':'INVALID_USER'})
    
    def get(self, request):
        
