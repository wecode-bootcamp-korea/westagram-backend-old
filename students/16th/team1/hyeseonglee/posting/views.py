import json
import re
from django.http      import JsonResponse
from django.views     import View

from posting.models   import Post, Comment
from user.models      import User


class PostView(View):
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = User.objects.get(email=data['email'])
            title      = data['title']
            content    = data['content']
            image_url  = data['image_url']

            p = re.compile('^([12]\\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\\d|3[01]))$')

            if not title and content and image_url:
                return JsonResponse({'MESSAGE': "YOUR REQUEST IS NOT ADEQUATE!"},status=400)
            
            if not Post.objects.filter(title=title).exists():
                Post.objects.create(
                                    user      = user, # 객체로 지정해야함 다른 속성값으로 하면 오류 발생함!
                                    title     = title,
                                    content   = content,
                                    image_url = image_url,
                                    )
                return JsonResponse({'MESSAGE': 'POST REQUEST SUCCEEDED!'}, status=200)
            return JsonResponse({'MESSAGE': 'TITLE ALREADY EXISTS!'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'},status=400)

        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE ERROR OCCURED!'},status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'USER DOES NOT EXISTS!'},status=400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'POST DOES NOT EXISTS!'},status=400)

        
    def get(self, request):
        try:
            posts  = Post.objects.all()
            post_list = []

            for i in posts:
                post_list.append(
                     {
                        'posts.id'        :i.id,
                        'posts.user'      :i.user.email,
                        'posts.title'     :i.title,
                        'posts.content'   :i.content,
                        'posts.created'   :i.created_dt,
                        'posts.image_url' :i.image_url,
                    }
                )
            return JsonResponse({'RESULT':post_list }, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'},status=400)

        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE ERROR OCCURED!'},status=400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'POST DOES NOT EXISTS!'},status=400)

class CommentView(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)

            user    = User.objects.get(email=data['email'])
            post    = Post.objects.get(title=data['post'])

            content = data['content']
            title   = data['title']
            
            if  not Comment.objects.filter(title=title) and content :
                Comment.objects.create(
                    user    = user,
                    post    = post,
                    author  = email,
                    title   = title,
                    content = content,
                )
                return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
            return JsonResponse({'MESSAGE': '동일 제목No! 내용 입력 해주세요!'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'},status=400)

        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE ERROR OCCURED!'},status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'USER DOES NOT EXISTS!'},status=400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'POST DOES NOT EXISTS!'},status=400)

    def get(self, request, pk):
        try:
            post     = Post.objects.get(pk=pk)
            comments = post.comment_set.all()

            if not comments.exists():
                return JsonResponse({"MESSAGE":'댓글이 없습니다'}, status=200)
            
            comment_list = []
            for i in comments:
                comment_list.append(
                    {
                        'comment.id'            : i.id,
                        'comment.user.id'       : i.user.id,
                        'comment.post.id'       : post.id,
                        'comment.user.email'    : i.user.email,
                        'comment.title'         : i.title,
                        'comment.content'       : i.content,
                        'comment.created'       : i.created_dt,
                    },
                )
            return JsonResponse({'댓글': comment_list },status=200) # JsonResponse안에 리스트를 넣어줘야합니다!
        
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'},status=400)

        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE ERROR OCCURED!'},status=400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'POST DOES NOT EXISTS!'},status=400)