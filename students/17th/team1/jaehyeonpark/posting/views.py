import json

from django.http      import JsonResponse
from django.views     import View
from django.db.utils  import DataError
from django.db.models import Q

from posting.models   import Post
from user.models      import User

class PostView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data.get('email')
            phone_number = data.get('phone_number')
            account      = data.get('account')
            image_url    = data['image_url']

            if not (email or phone_number or account):
                return JsonResponse({'message':'NO_USER_VALUE'}, status=400)
                
            if User.objects.filter(Q(email=email)|Q(phone_number=phone_number)|Q(account=account)).exists():
                user = User.objects.get(Q(email=email)|Q(phone_number=phone_number)|Q(account=account))
                Post.objects.create(user=user, image_url=image_url)
                return JsonResponse({'message':'SUCCESS'}, status=200)
            
            return JsonResponse({'message':'INVALID_USER'}, status=400)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except DataError:
            return JsonResponse({'message':'DATA_ERROR'}, status=400)
    
class ShowView(View):
    def get(self, request):
        try:
            posts   = Post.objects.all()
            results = []
            
            for post in posts:
                results.append(
                    {
                    "account":post.user.account,
                    "image_url":post.image_url
                    }
                )

            return JsonResponse({'results':results}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)