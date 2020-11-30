import json
from django.http        import JsonResponse
from django.views       import View
from .models            import Broad, Comments
from user.models        import Users

class Post(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = Users.objects.filter(name=data['name'],email=data['email'])
            
            # pk = user_id.pk
            if user.exists():
                Broad.objects.create(
                    title = data['title'],
                    photo = data['photo'],         
                    name = Users.objects.get(name=data['name'],email=data['email'])

                )
                return JsonResponse({'message':'게시물 업로드 완료'},status=200)
            else:
                return JsonResponse({'message':'로그인이 필요합니다'},status=400)
               
        except Exception as ex:
                return JsonResponse({'error':f'{ex}'},status=200)
    
    def get(self,request):
        broad_data = Broad.objects.values()
        return JsonResponse({'users':list(broad_data)},status=200)

class Comment(View):
    def post(self, request):
        key = ('user_id', 'post_id', 'content')
        data = json.loads(request.body)
        try : 
            user = Users.objects.filter(name=data['name'],email=data['email'])
            # user_id = user.id
            
            if user.exists():
                Comments.objects.create(
                    content = data['content'],
                    name = Users.objects.get(name=data['name']),
                    broad = Broad.objects.get(id=data['post_id']),
                )
                return JsonResponse({'message':'댓글 등록'},status=400)
            
            else:
                return JsonResponse({'error':'등록된 유저가 아닙니다, 로그인해주세요'},status=400)
        
        except Exception as ex:
            return JsonResponse({'error':f'{ex}'},status=400)



        
