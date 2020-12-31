import json
import re
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from posting.models   import Post
from user.models      import User


class PostView(View):
    def post(self, request):
        try:
            data       = json.loads(request.body)
            
            user       = User.objects.get(email=data['email'])
            email      = data['email']
            title      = data['title']
            content    = data['content']
            created_dt = data['created_dt']
            image_url  = data['image_url']
 

            p = re.compile('^([12]\\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\\d|3[01]))$')

            if not data and user and title and content and created_dt and image_url:
                return JsonResponse({'MESSAGE': "YOUR REQUEST IS NOT ADEQUATE!"},status=400)

            if not p.match(created_dt):
                return JsonResponse({'MESSAGE':'DATE TIME ERROR!'},status=400)
            
            if not Post.objects.filter(title=title).exists():
                Post.objects.create(
                                    user       =user,
                                    email      =email,
                                    title      =title,
                                    content    =content,
                                    created_dt =created_dt,
                                    image_url  =image_url,
                                    )
                return JsonResponse({'MESSAGE': 'POST REQUEST SUCCEEDED!'}, status=200)

            return JsonResponse({'MESSAGE': 'TITLE ALREADY EXISTS!'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'},status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'USER DOES NOT EXISTS!'},status=400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'POST DOES NOT EXISTS!'},status=400)

        
    def get(self, request):
        try:
            posts  = Post.objects.all()
            post_list = []
            for i in posts:
                print(i.user.email,'\n\n\n\n\n\n\n\n\n\n')
                post_list.append(
                     {
                        'posts.id'        :i.id,
                        'posts.user'      :i.user.email,
                        'posts.email'     :i.email,
                        'posts.title'     :i.title,
                        'posts.content'   :i.content,
                        'posts.created'   :i.created_dt,
                        'posts.image_url' :i.image_url,
                    }
                )
            return JsonResponse({'RESULT':post_list }, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'POST DOES NOT EXISTS!'},status=400)
