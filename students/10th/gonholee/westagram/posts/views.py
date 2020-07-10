import json
from django.http    import JsonResponse
from django.views   import View
from posts.models   import Post,Comment
from users.models   import User

class PostRegister(View):
    def post(self,request):
        data = json.loads(request.body)
        
        if data.get('email',None) == None or data.get('password',None) == None:
            return JsonResponse({'message':'email or password is vacant'},status=401)
        
        if data.get('post_text',None) == None or data.get('image_url') == None:
            return JsonResponse({'message':'fill your image url or post text'},status=401)

        if User.objects.filter(id=data['user_id']).exists():
            Post(
                post_text   =   data['post_text'],
                image_url   =   data['image_url'],
                user_id     =   data['user_id']
                ).save()

            return JsonResponse({'message':'Post Regist Success'},status=200)

        return JsonResponse({'message':'INVALID_User_id'},status=401)

class CommentRegister(View):
    def post(self,request):
        data = json.loads(request.body)
        
        if Post.objects.filter(id=data['id']).exists():
            Comment(
                comment_text    =   data['comment_text'],
                post_id         =   data['id']
            ).save()
            return JsonResponse({'message':'Comment Regist Success'},status=200)
        
        return JsonResponse({'message':'INVALID_Post_id'},status=401)

class PostLike(View):
    def post(self,request):
        data = json.loads(request.body)
        
        if Post.objects.filter(id=data['id']).exists():
            target_post         =   Post.objects.get(id=data['id'])
            target_post.hearts  +=  1
            target_post.save()
            return JsonResponse({'message':f"Like post(id:{data['id']})"},status=200)
        
        return JsonResponse({'message':'INVALID_Post_id'},status=401)
