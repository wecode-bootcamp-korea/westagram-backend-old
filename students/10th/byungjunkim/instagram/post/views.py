import json

from django.views import View
from django.http import JsonResponse
from django.db import OperationalError
from django.core.exceptions import ObjectDoesNotExist
from user.models import User
from .models import Post,Comment

class PostView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            Post(
                user=User.objects.get(id=data['user_id']),
                title=data['title'],
                text=data['text']
            ).save()
            return JsonResponse({'message':'SUCCESS'},status=200)
        except ValueError:
            return JsonResponse({'message':'WRONG_VALUE'},status=400)    
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'},status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'message':'DONT_EXIST'},status=401)

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            Comment(
                user=User.objects.get(id=data['user_id']),
                post=Post.objects.get(id=data['post_id']),
                text=data['text']
            ).save()
            return JsonResponse({'message':'SUCCESS'},status=200)
        except ValueError:
            return JsonResponse({'message':'WRONG_VALUE'},status=400)    
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'},status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'message':'DONT_EXIST'},status=401)
            
class ThumbsView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            Comment(
                user=User.objects.get(id=data['user_id']),
                post=Post.objects.get(id=data['post_id'])
            )
            return JsonResponse({'message':'SUCCESS'},status=200)
        except ValueError:
            return JsonResponse({'message':'WRONG_VALUE'},status=400)    
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'},status=400)
        except TypeError:
            return JsonResponse({'message':'WRONG_TYPE'},status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'message':'DONT_EXIST'},status=401)