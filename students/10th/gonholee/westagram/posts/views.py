import json
from django.http    import JsonResponse
from django.views   import View
from .models        import Post, Comment
from users.models   import User

class PostRegister(View):
    def post(self,request):
        data = json.loads(request.body)
        if data.get('email',None) == None or data.get('password',None) == None:
            return JsonResponse({'message':'email or password is vacant'},status=401)
        if data.get('post_text',None) == None or data.get('image_url') == None:
            return JsonResponse({'message':'fill your image url or post text'},status=401)
        try:
            if User.objects.filter(email=data['email']).exists():
                login_user = User.objects.get(email=data['email'])
                if login_user.password == data['password']:
                    pass
                else:
                    return JsonResponse({'message':'INVALID_USER'},status=401)
            else:
                return JsonResponse({'message':'INVALID_USER'},status=401)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'},status=400)

        # Login Success Case
        Post(
            post_text   =   data['post_text'],
            image_url   =   data['image_url'],
            user_id     =   login_user.id
            ).save()
        return JsonResponse({'message':'Post Regist Success'},status=200)

class CommentRegister(View):
    def post(self,request):
        data = json.loads(request.body)
        if Post.objects.filter(id=data['id']).exists():
            Comment(
                comment_text    =   data['comment_text'],
                post_id         =   data['id']
            ).save()
            return JsonResponse({'message':'Comment Regist Success'},status=200)
        else:
            return JsonResponse({'message':'INVALID_Post_id'},status=401)

class PostLike(View):
    def post(self,request):
        data = json.loads(request.body)
        if Post.objects.filter(id=data['id']).exists():
            target_post         =   Post.objects.get(id=data['id'])
            target_post.hearts  +=  1
            target_post.save()
            return JsonResponse({'message':f"Like post(id:{data['id']})"},status=200)
        else:
            return JsonResponse({'message':'INVALID_Post_id'},status=401)

