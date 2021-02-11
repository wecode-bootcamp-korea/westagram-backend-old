import json

from django.views import View
from django.http  import JsonResponse

from user.models  import User
from .models      import Post, Comment


# TimeStampedModel을 상속 받아서 데이터가 생성될 때, 수정될 때의 시간이 기록되도록 만들자

class Post_View(View): #게시글 
    def post(self,request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(email = data['email']).exists(): # 이메일 객체가 있으면
                member = User.objects.get(email = data['email']) # 이메일데이터를 갖고 있는 User를 가져와서 Post의 email에 넣어준다
                Post( # post게시글에서 적은걸 저장해줌
                    email    = member,
                    content = data['content'],
                    img_url = data['img_url'],
                ).save() # 저장
                return JsonResponse({'message':'SUCCESS'},status = 200)
            else: #이메일이 없으면 권한을 주지 않음
                return JsonResponse({'message':'UNAUTHORIZED'},status = 401) 
        except Exception as exceptions: 
            return JsonResponse({'message':exceptions},status = 400) #디비저장할때 발생하는 오류가 일어날때 처리

class Post_List_View(View): #게시글 목록
    def get(self,request):
        post_list = Post.objects.values()
        return JsonResponse({'post_list':list(post_list)}, status = 200)

class Comment_View(View): # 댓글 
    def post(self,request, post_id):
        data = json.loads(request.body)

        try:
            if User.objects.filter(email = data['email']).exists() or Post.objects.filter(id = post_id).exists(): #이메일 혹은 게시글 id가 존재하는지 따져줘야함
                member = User.objects.get(email = data['email']) #있다면 이메일 데이터를 member변수에 넣어줌
                post = Post.objects.get(id = post_id) # 게시글 아이디도 있어야지 그 게시글에 댓글달수있음
                Comment(
                    email    = member,
                    post     = post,
                    comment   = data['comment'],
                ).save() #댓글 저장함
                return JsonResponse({'message':'SUCCESS'},status = 200)
            else:
                return JsonResponse({'message':'UNAUTHORIZED'},status = 401)  #두개 중 하나라도 존재x -> 예외처리시켜
        except Exception as exceptions:
            return JsonResponse({'message':exceptions},status = 400) 

class Comment_List_View(View): #댓글 목록
    def get(self,request, post_id): 
        if Post.objects.filter(id = post_id).exists(): 
            comment_list = Comment.objects.values().filter(post = post_id)
            return JsonResponse({'comment_list': list(comment_list)}, status = 200)
       

       #오류났었던것: 객체가 같으면 가져오는 줄 알고 객체를 그대로 get해서 넣었는데,
       #get하면 리스트로 나와버림
       #id값(다른테이블의pk를 fk로 가져와서?)을 가져오는데 pk값만 넣어주면 알아서 찾아옴

