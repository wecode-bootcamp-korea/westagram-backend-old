import json

from django.http   import HttpResponse, JsonResponse
from django.views  import View

from User.models  import Userinfo
from .models      import UserPosting


class ContentSignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if Userinfo.objects.filter(name = data['name']).exists():
                user = Userinfo.objects.get(name = data['name'])  
                image_url = data['image_url']

                UserPosting.objects.create(
                        user_ID   = user,
                        image_url = image_url
                        )
                return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)
            return JsonResponse({"MESSAGE" : "INVALID_NAME"}, status=400)
        except KeyError:
            return JsonResponse({"MESSAGE":"INVALID_KEY"}, status=400)

class ContentGetView(View):
    def get(self, request):
        content_data = UserPosting.objects.values()
        
        return JsonResponse({"content_data": list(content_data)},status=200)
