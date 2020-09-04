import json
from django.views import View
from django.http  import JsonResponse
from .models      import Posting
from user.models  import Users

class RegisterPost(View):
    def post(self, request):
        data = json.loads(request.body)
        
        if not Users.objects.get(email=data['email']):
            return JsonResponse({'message':'NO PERMISSION'}, status=400)

        else:
            Posting(
                writer         = Users.objects.get(email=data['email']),
                contents       = data['contents'],
                published_date = data['published_date'],
                images_url     = data['images_url']
            ).save()

        return JsonResponse({'message':'SUCCESS'}, status=200)


class Posting(View):
    def get(self, request):
        posting_data = RegisterPost.objects.values()
        return JsonResponse({'posting': list(posting_data)}, status=200)