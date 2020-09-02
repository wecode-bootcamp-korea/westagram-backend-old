from django.views import View
from django.http  import JsonResponse

from .models      import PostMedia, Photo

def post(self, request):
        data                    = json.loads(request.body)
        MINIMUM_PASSWORD        = 8
        query_data              = Users.objects
        #query_data              = Users.objects.values('name', 'email', 'phon_number')
        
        PostMedia(
        title             = data['title'],
        content           = data['content'],
        user              = request.users
        ).save()
        
        return JsonResponse({'message':'SUCCESS'}, status=200)
    
    def get(self, request):
        user_data = Users.objects.values()

        return JsonResponse({'users':list(user_data)}, status=200)

class Create(View):
    def post(self, request):
        
            post = Post()
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.pub_date = timezone.datetime.now()
            post.user = request.user
            post.save()
            # name 속성이 imgs인 input 태그로부터 받은 파일들을 반복문을 통해 하나씩 가져온다 
            for img in request.FILES.getlist('imgs'):
                # Photo 객체를 하나 생성한다.
                photo = Photo()
                # 외래키로 현재 생성한 Post의 기본키를 참조한다.
                photo.post = post
                # imgs로부터 가져온 이미지 파일 하나를 저장한다.
                photo.image = img
                # 데이터베이스에 저장
                photo.save()
            return redirect('/detail/' + str(post.id))
    