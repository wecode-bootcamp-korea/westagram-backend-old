import jwt
import json

from django.http            import JsonResponse

from .models                import PostMedia, Photo
from user.models            import User
from westagram.settings     import SECRET_KEY, ALGORITHM

def authorization(func):
    def wrap(self, request):
        user_token              = json.loads(request.body)['Authorization'] #header로 바꿀 예정
        decoded_jwt             = jwt.decode(user_token, SECRET_KEY, algorithm= ALGORITHM)
        
        if User.objects.filter(id = decoded_jwt['user_id']):
            login_user_id       = decoded_jwt['user_id']
            return func(self, request, login_user_id)
        else:
            return JsonResponse({'message':'INVALID_USER'}, status= 401)
    return wrap