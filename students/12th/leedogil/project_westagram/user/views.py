from .models       import Users

class SignUpView(View):
  def post(self, request):
    data = json.loads(request.body)
    if 'email' or 'password' not in data.keys()
      return JsonResponse({"message": "KEY_ERROR"},STATUS=400)
    elif '@' and '.' not in data['email']
      return JsonResponse({"message":"email validation"},status=400)
    elif len(data['password'] < 8
      return JsonResponse({"message":"password validation"},status=400)
    else:
      Users(
        phone    = data['phone']
        name     = data['name'],
        email    = data['email'],
        password = data['password']
      ).save() 

    return JsonResponse({'message':'SUCCESS'},
    status=200)

  def get(self, request):
    user_data = Users.objects.values()
    return JsonResponse({'users':list(user_data)},status=200)
