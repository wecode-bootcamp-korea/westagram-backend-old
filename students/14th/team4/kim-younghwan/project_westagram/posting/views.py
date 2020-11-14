import json

from django.http        import JsonResponse, HttpResponse
from django.views       import View

from .models            import Broads, Comments
from user.models        import Accounts, Broadlikes
from user.utils         import login_decorator



class Post(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:             
            #-----게시물 올리기-----#
            user = Accounts.objects.filter(name=data['name'],email=data['email'])
            if user.exists():
                Broads.objects.create(
                    title = data['title'],
                    photo = data['photo'],         
                    name = Accounts.objects.get(name=data['name'],email=data['email']),
                )
                return JsonResponse({'message':'게시물 업로드 완료'},status=200)
            
            return JsonResponse({'message':'로그인이 필요합니다'},status=400)
        except Exception as ex:
            return JsonResponse({'error':f'{ex}'},status=400)    

class Like(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
             #-----좋아요-----#
            
            user = Accounts.objects.get(email=data['email']) 
            like_list = user.likes.all()
            post= Broads.objects.get(id=data['post_id'])
            #user_exist = Broadlikes.objects.filter(account=user.id).exists()
            post_exist = post.like.filter(email=user.email)
           
            # 좋아요 취소 & 좋아요 클릭
            if post_exist:
                post.like.remove(user)
                return JsonResponse({'message':f'({user.name}) 님이 게시물({post.id}) 좋아요 취소'},status=201)
                
            else:
                post.like.add(user)
                likes_num = post.like.count()
                return JsonResponse({'message':f'({user.name}) 님이 게시물({post.id}) 좋아요','좋아요':f'{likes_num}개'},status=201)
            
            # if Broadlikes.objects.filter(broad=post.id).exists():
            #     likes_num =post.like.count()
            #     Broads.objects.create(likecount=likes_num)
            #     return JsonResponse({'post_id':f'{post.id}','좋아요':f'{likes_num}'})
        
        except KeyError:
            return JsonResponse({'message':'KEYERROR'},status=400)
    
    
    @login_decorator
    def get(self,request):
        broad_data = Broads.objects.values()
        return JsonResponse({'Accounts':list(broad_data)},status=200)

class Comment(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try : 
            user = Accounts.objects.filter(name=data['name'],email=data['email'])
            # user_id = user.id
            
            if user.exists():
                Comments.objects.create(
                    content = data['content'],
                    name = Accounts.objects.get(name=data['name']),
                    broad = Broads.objects.get(id=data['post_id'])
                )
                return JsonResponse({'message':'댓글 등록'},status=400)
            
            else:
                return JsonResponse({'error':'등록된 유저가 아닙니다, 로그인해주세요'},status=400)
         
        except Exception as ex:
            return JsonResponse({'error':f'{ex}'},status=400)




        
