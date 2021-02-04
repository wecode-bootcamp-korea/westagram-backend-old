import json, re

from json.decoder       import JSONDecodeError

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from .models            import Posting
from user.models        import User
from user.utils         import LoginAuthorization

class PostingView(View):
    def get(self, request):
        postings        = Posting.objects.all()
        posting_list    = []

        for posting in postings :
            posting_info = {
                #    'id'            : posting.id,
                    'name'          : User.objects.get(id=posting.user_id).name,
                    'image_url'     : posting.image_url,
                    'descrption'    : posting.description,
                    }
            posting_list.append(posting_info)

        return JsonResponse({'당신의 게시물!' : posting_list}, status=200)
    @LoginAuthorization
    def post(self, request):
        try:
            data        = json.loads(request.body)
            name        = data['name']
            image_url   = data['image_url']
            description = data.get('description', None)
            if request.user != User.objects.get(name=name):
                return JsonResponse({'message' : 'INVALID_USER'}, status=400)
            user        = request.user.id

            Posting.objects.create(
                    user_id = user,
                    image_url = image_url,
                    description = description
                    )
            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message' : '누구냐 넌'}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'message' : 'NOTHING_INPUT'}, status=400)
