import json

from django.views import View
from django.http  import JsonResponse

from .models import User


class SignUpView(View):
  def post(self, request):
    data = json.loads(request.body)

    try:
      name         = data['name']
      user_name    = data['user_name']
      email        = data['email']
      password     = data['password']
      phone_number = data['phone_number']

      if not '@' or not '.' in data['email']:
        return JsonResponse({'message': 'not valid email'}, status=400)
      
      if len(data['password']) < 8:
        return JsonResponse({'message': 'not valid password'}, status=400)
      
      if User.objects.filter(user_name = user_name).exists():
        return JsonResponse({'message': 'user_name already exist'}, status=400)

      User.objects.create(
        name         = name,
        user_name    = user_name,
        email        = email,
        password     = password,
        phone_number = phone_number,
      )
      
    except KeyError:
      return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    else:
      return JsonResponse({'message': 'SUCCESS'}, status=200)
