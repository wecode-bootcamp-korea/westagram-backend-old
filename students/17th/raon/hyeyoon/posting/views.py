import json

from django         import views
from django.views   import View
from django.http    import JsonResponse,HttpResponse

from .models        import Posting
from user.models    import Account

class ContentSignUpView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            name        = data['name']
            image_url   = data['image_url']
            description = data['description']

            if Account.objects.filter(name = name).exists():
                user = Account.objects.get(name = name)

                Posting.objects.create(
                    account     = user,
                    image_url   = image_url,
                    description = description

                )

                return JsonResponse({"MESSAGE":"SUCCESS"}, status = 200)
            return JsonResponse({"MESSAGE":"INVALID_USER"}, status = 401)
        except KeyError:
            return JsonResponse({"MESSAGE":"INVALID_KEY"}, status = 400)

class ContentGetView(View):
    def get(self, request):
        postings = Posting.objects.all()

        content_list = []
        for posting in postings:
            contents = {
                'user'        : posting.account.name,
                'image_url'   : posting.image_url,
                'create_date' : posting.create_date,
                'description' : posting.description
            }
            content_list.append(contents)
    
        return JsonResponse({"data":content_list}, status = 200)
