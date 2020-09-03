import json
from django.views import View
from django.http  import JsonResponse
from .models      import Users


class SignUp(View):
    def post(self, request):

        data     = json.loads(request.body)
        MIN_PWD  = 10

        set_data = User.objects.values('name', 'email', 'phone_number')
        
        if filter_data in set_data:
            return JsonResponse({'message': 'Already existed'}, status = 400)

        if len(data['password']) < MIN_PWD:
            return JsonResponse({'message':'Minimum length of pwd is 10'}, status=400)

        if '@' or '.' not in data['email']:
            return JsonResponse({'message':"please check if '@' or '.' are included properly"}, status =400)

        if 'email' not in data.keys():
            return JsonResponse({'message':'No such address'}, status = 400)

        else:
            Users(
                name        = data['name'],
                phone_number= data['phone_number'],
                email       = data['email'],
                password    = data['password'],
            ).save()


            return JsonResponse({'message':'SUCCESS'}, status=200)
    
    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({"users":list(user_data)}, status=200)



