import json
from ast           import literal_eval

from django.views  import View
from django.http   import JsonResponse

from .models       import Post, PostImage
from user.models   import User

class PostCreateView(View):
    def post(self, request):
        try :
            data = json.loads(request.body)
            user = User.objects.get(nickname = data['writer'])
            
            post = Post.objects.create(
                title   = data['title'],
                content = data['content'],
                writer  = user
            )
            
            try:
                image_urls = literal_eval(data['image_url'])       #String 형태의 image_url을 list로 변환

                for image_url in image_urls:
                    PostImage.objects.create(image_url = image_url, post = post)
            except:
                    pass

            return JsonResponse({'MESSAGE :':"SUCCESS"},status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 400)

class PostReadView(View):
    def get(self, request):
        try:
            posts    = Post.objects.all()
            req_list = []

            for post in posts:
                images = post.postimage_set.all()

                if images.exists():
                    image_list = [ image.image_url for image in images ]  
                else:
                    image_list = []
                
                req_dict   = {
                    'id'        : post.id,
                    'title'     : post.title,
                    'content'   : post.content,
                    'writer'    : post.writer.nickname,
                    'image_url' : image_list,
                    'created_at': post.created_at,
                    'updated_at': post.updated_at,
                }
                req_list.append(req_dict)

            return JsonResponse({'menus':req_list},status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)