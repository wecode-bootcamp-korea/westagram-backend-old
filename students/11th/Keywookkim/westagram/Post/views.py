import json, jwt

from django       import forms
from django.views import View
from django.http  import JsonResponse

from .models      import Bulletin, Comment
from User.models  import User

class Post(View) :
    def post(self, request):
        data    = json.loads(request.body)

        try :
            if User.objects.filter(id = data['email']).exists() :
                account = User.objects.get(id = data['email'])
            else :
                return JsonResponse({'message':'Invalid User'}, status=400) 
            b = Bulletin(
                account    = account,
                title      = data['title'],
                context    = data['context'],
                img_url    = data['img_url'],
            )
            if data['title'] == '' or data['context'] == '' :
                return JsonResponse({'message':'Invalid title or context'}, status=400) 
            b.save()
            return JsonResponse({'message':'Posting Upload SUCCESS!'}, status=200)
        except KeyError :
            return JsonResponse({'message':'KEY_ERROR'}, status=400) 
        except ValueError :
            return JsonResponse({'message':'Value_ERROR'}, status=400)     

    def get(self, request):
        posting_data = Bulletin.objects.values()
        return JsonResponse({'Recent post':list(posting_data)}, status=200)   


class CommentView(View) :
    def post(self, request) :
        data = json.loads(request.body)
        try : 
            if User.objects.filter(id = data['email']).exists() :
                account = User.objects.get(id = data['email']) 
            if Bulletin.objects.filter(id = data['bulletin']).exists() :
                bulletin = Bulletin.objects.get(id = data['bulletin'])
            else :
                return JsonResponse({'message':'Invalid User or Post'}, status=400) 
            c = Comment(
                account = account,
                bulletin = bulletin,
                commentbox = data['commentbox'],
            )
            c.save()
            return JsonResponse({'message':'Comment Upload SUCCESS!'}, status=200)  
        except KeyError :
            return JsonResponse({'message':'KEY_ERROR'}, status=400) 
        except ValueError :
            return JsonResponse({'message':'Value_ERROR'}, status=400) 

    def get(self,request) :
        comment_data = Comment.objects.values()
        return JsonResponse({'Recent comment':list(comment_data)}, status=200)



