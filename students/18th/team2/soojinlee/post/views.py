from django.http  import JsonResponse, HttpResponse
from django.views import View

from user.models  import User
from .models      import post


class PostView(view):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            user         = data['user']
            image        = data['image']

            user = User.objects.get(email = user)
            Post.objects.create(user=data['email'], image=data['image'])
            return JsonResponse({'message': 'SUCCESS', status=201})

        except KeyError :
            return JsonResponse({"message": "게시글 형식 확인하세요"}, status=400)


    def get(self, request):

        post = Post.objects.all()

        result = []

            data         = json.loads(request.body)
            user         = data['user']
            image        = data['image']

            user = User.objects.get(email = user)
        
            return JsonResponse({'message': 'SUCCESS', status=200})
