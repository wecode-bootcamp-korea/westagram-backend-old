import json

from django.http        import JsonResponse, HttpResponse
from django.views       import View

from .models            import Broads, Comments
from user.models        import Accounts
from user.utils         import login_decorator



class Post(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = Accounts.objects.filter(name=data['name'],email=data['email'])
    
            if user.exists():
                Broads.objects.create(
                    title = data['title'],
                    photo = data['photo'],         
                    name = Accounts.objects.get(name=data['name'],email=data['email'])

                )
                return JsonResponse({'message':'게시물 업로드 완료'},status=200)
            else:
                return JsonResponse({'message':'로그인이 필요합니다'},status=400)
               
        except Exception as ex:
                return JsonResponse({'error':f'{ex}'},status=200)
    
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



        
