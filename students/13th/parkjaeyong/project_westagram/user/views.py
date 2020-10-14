import json
from django.views import View 
from django.http  import JsonResponse 
from .models      import Users

class SignUpView(View):
    
    def post(self , request):
        data =json.loads(request.body)
        try:
                
                name         = data["name"]
                email        = data["email"]
                phone_number = data["phone_number"]
                password     = data["password"]

                a=Users.objects.all()
                for x in a :
                    if name==x.name or email==x.email or phone_number==x.phone_number:
                        return JsonResponse({"Message":"joongbok error"},status=400)
                    
                if len(password)<=8 :
                    return JsonResponse({"Message":"password not invalied"},status=400)
                if email.find('@')==-1 or email.find('.')== -1 :
                    return JsonResponse({"Message":"Email not invalied"},status=400)


                Users.objects.create(name=name, email=email, phone_number=phone_number, password=password)

                return JsonResponse({"Message":"SUCSESS"} , status=200)
            
        except KeyError:
            return  JsonResponse({"Message":"KEY_ERROR"} , status=400)


    
       



 
