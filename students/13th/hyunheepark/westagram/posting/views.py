import json

from django.views   import View
from django.http    import JsonResponse
from posting.models import Post,Comment
from user.models    import User


class PostView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)

            #user_id = User.objects.get(name=data['name'])
            user_id = data['user_id']
            content = data['content']
            img_url = data['img_url']
       
            if not img_url:
                 return JsonResponse({'MESSAGE':'이미지를 첨부하세요.'},status=400)
            
            else:
                Post.objects.create(
                    #user_id = user_id.id,
                    user_id = user_id,
                    content = content,
                    img_url = img_url
                )
        
            return JsonResponse({'MESSAGE':'SUCCESS'},status=201)
        except KeyError:
            return JsonResponse({'MESSAGE':'KeyError'},status=400)

    def get(self,request):
        #print(Post.objects.values())
        #print(list(Post.objects.values()))
        return JsonResponse({'POST LIST':list(Post.objects.values())},status=201)



class CommentView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            print(data)            
            #if not data['uer_id']:
            #   return JsonResponse({'MESSAGE':'로그인 하세요.'},status=400)
            
            #if not data['comment_content']:
            #    return JsonResponse({'MESSAGE':'댓글 내용을 작성해주세요.'},status=400)

            #else:
            Comment.objects.create(
                    user_id = data['user_id'],
                    comment_content = data['comment_content'],
                    post_id = data['post_id'],
                    )
            return JsonResponse({'MESSAGE':'SUCCESS'},status=201)




        except KeyError:
            return JsonResponse({'MESSAGE':'KEYERROR'},status=400)
        except ValueError:
            return JsonRecponse({'MESSAGE':'VALUEERROR'},status=400)


    def get(self,request):
        comment_values = Comment.objects.values()
        first_post = (Post.objects.all())[0]
        comments = Comment.objects.filter(post_id = first_post.id).values(
            'user_id',
            'comment_content',
            'created_at'
            )

        return JsonResponse({'MESSAGE':list(comments)},status=201)
            
