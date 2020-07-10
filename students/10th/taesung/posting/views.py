import json
from django.views import View
from django.http import JsonResponse
from .models import Article 

class post(View):

    def post(self, request):

        try:
            data = json.loads(request.body)
            Article(
                    head = data['head'],
                    body = data['body']
                    ).save()

            return JsonResponse({'message':'SUCCESS'}, status=200)
        
        except Exception as e:
            return JsonResponse({"message": f"{e}"}, status = 401)
