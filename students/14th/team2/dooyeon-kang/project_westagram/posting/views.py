import json

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from posting.models import Posting
from user.models import User

class PostingView(View):

    def post(self, request):
        data = json.loads(request.body)

        try:
            input_user  = data['user_id']
            image_url   = data['image_url']
            description = data['description']
        except Exception as error_message:
            return JsonResponse({'message': error_message}, status = 400)

        try:
            user = User.objects.get(id=input_user)
        except Exception:
            return JsonResponse({'message': 'INVALID USER'}, status = 401)

        try:
            Posting(
                image_url   = image_url,
                description = description,
                user        = user,
            ).save()

            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except Exception:
            return JsonResponse({'message': 'Somthing wrong'}, status = 400)

    def get(self, request):
        posts = Posting.objects.values()

        try:
            result = [
                {'user': {
                    'user_id': post['user_id'],
                    'username': User.objects.get(id=post['user_id']).name
                 },
                 'img_url': post['image_url'],
                 'description': post['description'],
                 'created_at': post['created_at']} for post in posts
            ]

            return JsonResponse({'result': result}, status = 200)

        except Exception as error_message:
            return JsonResponse({'message': error_message}, status = 400)
