import json

from django         import views
from django.views   import View
from django.http    import JsonResponse,HttpResponse

from .models        import Posting, Comment
from user.models    import Account

class ContentView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            email       = data['email']
            image_url   = data['image_url']
            description = data['description']

            if Account.objects.filter(email = email).exists():
                user = Account.objects.get(email = email)

                Posting.objects.create(
                    account     = user,
                    image_url   = image_url,
                    description = description

                )

                return JsonResponse({"MESSAGE":"SUCCESS"}, status = 200)
            return JsonResponse({"MESSAGE":"INVALID_USER"}, status = 401)
        except KeyError:
            return JsonResponse({"MESSAGE":"INVALID_KEY"}, status = 400)


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
    
        return JsonResponse({"data":content_list}, status = 201)

class CommentView(View):
    def post(self,request):
        try:
            data        = json.loads(request.body)
            email       = data['email']
            comment     = data['comment']
            post_id     = data['post_id']

            if not Account.objects.filter(email = email).exists():
                return JsonResponse({"MESSAGE":"INVALID_USER"}, status = 401)
            user = Account.objects.get(email = email)
        
            if not Posting.objects.filter(id = post_id).exists():
                return JsonResponse({"MESSAGE":"INVALID_POST"}, status = 401)
            post = Posting.objects.get(id = post_id)

            if comment == "":
                return JsonResponse({"MESSAGE":"NO_COMMENTS"}, status = 401)
    
            Comment.objects.create(
                user    = user,
                post    = post,
                comment = comment
            )
            return JsonResponse({"MESSAGE":"SUCCESS"}, status = 200)
        
        except KeyError:
            return JsonResponse({"MESSAGE":"INVALID_KEY"}, status = 400)
    
    def get(self,request):
        comments = Comment.objects.all()
        comment_list = []
        for comment in comments:
            comment_info = {
                'comment':comment.comment,
                'posting_id':comment.post_id
            }
        comment_list.append(comment_info)


        return JsonResponse({"comment":comment_list}, status = 201)