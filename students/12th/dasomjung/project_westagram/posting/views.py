import json
from django.views import View
from django.http  import JsonResponse
from .models      import Posting, Images
from user.models  import Users

class RegisterPost(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            if not Users.objects.get(email=data['email']):
                return JsonResponse({'message':'NO PERMISSION'}, status=400)

            else:
                posting = Posting.objects.create(
                writer         = Users.objects.get(email=data['email']),
                contents       = data['contents']
                )
                posting.save()

                Images(
                    images_url = data['images_url'],
                    posting = posting
                ).save()
            
                return JsonResponse({'message':'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class Posting(View):
    def get(self, request):
        posting_data = Posting.objects.values()
        return JsonResponse({'posting': list(posting_data)}, status=200)