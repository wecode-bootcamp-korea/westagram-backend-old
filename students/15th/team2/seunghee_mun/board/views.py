import json
from django.http             import JsonResponse
from django.views            import View
from django.core.serializers import serialize
from board.models            import Board, Comment
from user.models             import User

class BoardView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            # info validation
            title     = data['board_name']
            body_text = data['contents']
            image_url = data['image']
            
            # login_user validation
            user_post = User.objects.get(user_name=data['user']).id

            # title validation
            if Board.objects.filter(name=data['board_name']).exists():
                raise ValueError
            Board.objects.create(name=title, user_id=user_post, image_url=image_url, contents=body_text)
            return JsonResponse ({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'NOT_ENOUGH_INFO'}, status=401)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'NOT_MEMBER'}, status=403)

        except ValueError:
            return JsonResponse({'MESSAGE' : 'TITLE_OVERLAP'}, status=403)

    def get(self, request):
        # empty_board validation
        try:
            board_values = Board.objects.all().order_by('-id')
            get_data     = json.loads(serialize('json', board_values))
            return JsonResponse({'board' : get_data})
        except ValueError:
            return JsonResponse({'MESSAGE' : 'EMPTY_BOARD'}, status=400)

class CommentView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        #login_user validation
            user_comment = User.objects.get(user_name=data['user']).id

        # board validation
            board_comment                   = Board.objects.get(name=data['board_title']).id
            body_comment                    = data['comment_body']
            Comment.objects.create(board_id = board_comment, user_id=user_comment, body=body_comment)
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except NameError:
            return JsonResponse({'MESSAGE' : 'NO COMMENTS'}, status=400)
        
        except Board.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'THERE ARE NO BOARD'}, status=403)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'NOT_MEMBER'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'NO_INPUT_DATA'}, status=400)

    def get(self, request):
        first_board            = Board.objects.first()
        comment_values_first   = Comment.objects.filter(board_id=first_board)
        get_comment_first_data = json.loads(serialize('json', comment_values_first))
        return JsonResponse({'COMMENT' : get_comment_first_data })
