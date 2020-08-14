import json
from django.http import JsonResponse
from django.views import View
from .models import Posting
from account.models import Account
from posting.models import Posting
from posting.models import Comment

class PostingView(View): 
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = data['user']
            content    = data['content']
            img_url    = data['img_url']

            get_user = Account.objects.get(name = user)
            Posting(
                user       = get_user,
                content    = content,
                img_url    = img_url,
            ).save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        
        # DoesNotExist는 get에서 조건에 맞는 data가 없을 경우 발생됨. filter의 경우 [] return
        except Account.DoesNotExist:
            return JsonResponse({'message': 'Account_DoesNotExist'}, status = 401)    
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'JSON_TYPE_Error'}, status = 401)
        except ValueError:
            return JsonResponse({"message": "VALUSE_ERROR"}, status = 400)
    def get(self, request):
        posted_data = Posting.objects.values()
        # print(list(posted_data))
        return JsonResponse({'message': list(posted_data)}, status = 200)

class CommentView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            comment_user            =   data['user']
            comment_content         =   data['content']
            post_comment_id         =   data['post']  # post_id는 database에서 post의 id와 동일하게

            user_name               =   Account.objects.get(name = comment_user)
            post_id                 =   Posting.objects.get(id = post_comment_id)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        except Account.DoesNotExist: 
            return JsonResponse( {'message': 'Account_DoesNotExist'}, status = 401)
        except Posting.DoesNotExist:
            return JsonResponse( {'message': 'Post_DoesNotExist'}, status = 401)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'JSON_TYPE_Error'}, status = 401)
        except ValueError:
            return JsonResponse({"message": "VALUSE_ERROR"}, status = 400)
        Comment(
            user    = user_name,
            post    = post_id,
            content = comment_content
        ).save()
        
        return JsonResponse({'message':'COMMENT_SUCCESS'}, status=200)

    def get(self, request):
        try:
            if(Comment.objects.filter(post_id = "1").exists()):
                selected_data = Comment.objects.filter(post_id = "1").values()
                print(selected_data)
                if not selected_data:
                    return JsonResponse({'message': 'NO_COMMENT'})
                return JsonResponse({'message': list(selected_data)}, status = 200)
            else:
                return JsonResponse({'message': 'POST_NOT_EXIST'}, status = 401)
        except Comment.DoesNotExist:
            return JsonResponse( {'message': 'Comment_NOT_EXIST'}, status = 401)