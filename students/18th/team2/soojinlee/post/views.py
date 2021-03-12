import json

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q

from user.utils   import signin_required
from user.models  import User
from .models      import Post



class Posting(View):
    @signin_required
    def post(self, request):
        try:
            data         = json.loads(request.body)
            user         = data['user']
            image        = data['image']
            description  = data['description']

            signin_user = User.objects.get(Q(email=user)| Q(user_name=user) | Q(phone_number=user))
            print('2222222222')
            print(signin_user)
            print('222222222222')
            Post.objects.create( user = signin_user, image=image, description = description)
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError :
            return JsonResponse({"message": "게시글 형식 확인하세요"}, status=400)

# class PostView(View):

#     def get(self, request):

#         post = Post.objects.all()
        
#         result = []

#             user         = data['user']
#             image        = data['image']
        