import json
from django.http    import JsonResponse
from django.views   import View
from posts.models   import Post,Comment
from users.models   import User

class PostRegister(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            if data['user_id'] and data['post_text'] and data['user_id']:

                if User.objects.filter(id=data['user_id']).exists():

                    Post(
                        post_text   =   data['post_text'],
                        image_url   =   data['image_url'],
                        user_id     =   data['user_id']
                    ).save()
                    
                    return JsonResponse({'message':'Post Regist Success'},status=200)

                return JsonResponse({'message':'INVALID_User_id'},status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'},status=400)

class CommentRegister(View):
    def post(self,request):
        data = json.loads(request.body)
        
        try:
            if data['comment_text'] and data['post_id']:
                
                if Post.objects.filter(id=data['post_id']).exists():
                    Comment(
                        comment_text    =   data['comment_text'],
                        post_id         =   data['post_id']
                    ).save()
                    
                    return JsonResponse({'message':'Comment Regist Success'},status=200)
                
                return JsonResponse({'message':'INVALID_Post_id'},status=401)
        
        except KeyError:
            
            return JsonResponse({'message': 'KEY_ERROR'},status=400)

class PostLike(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            if data['post_id']:
                
                if Post.objects.filter(id=data['post_id']).exists():
                    target_post         =   Post.objects.get(id=data['post_id'])
                    target_post.hearts  +=  1
                    target_post.save()
                    
                    return JsonResponse({'message':f"Like post id:{data['post_id']}"},status=200)
                
                return JsonResponse({'message':'INVALID_Post_id'},status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'},status=400)
